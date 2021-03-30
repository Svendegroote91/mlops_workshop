"""Run hyperparameter tuning training jobs on AI platform."""

import asyncio
import datetime

import fire


import config
from helpers.aip import get_opt_hyperparams, read_aip_config, launch_train_job
from helpers.gcloud import gcs_list_dir
from steps.prepare_datasets import prepare_datasets


# You can change this parameter between 1 (only train a model for 1 single cover type) and 7
# (train a model for all cover types). Depending on the hyperparameter tuning config and the
# setting of this parameter, the number of different training jobs can become quite high!
N_MODELS_TO_TRAIN = 1


def get_args(gcs_bucket, run_name):
    return {
        'gcs_bucket': gcs_bucket,
        'run_name': run_name
    }


async def run(gcs_bucket, run_name):
    run_name = f'{run_name}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'
    gcs_run_path = f'gs://{gcs_bucket}/{run_name}'
    prepare_datasets(config.DATASET_NAME, gcs_run_path, config.TARGET_COL)

    # Launch the training jobs
    cover_types = sorted(gcs_list_dir(gcs_bucket, run_name)[:N_MODELS_TO_TRAIN])
    job_ids = []
    for cover_type in cover_types:
        gcs_csv_path = f'{gcs_run_path}/{cover_type}/raw_data.csv'
        gcs_output_path = f'{gcs_run_path}/{cover_type}/output'

        # Create AI Platform training job spec
        # https://cloud.google.com/ai-platform/training/docs/reference/rest/v1/projects.jobs#TrainingInput
        job_id = f'{run_name}_{cover_type}'
        training_input = read_aip_config('config/aip_config.yaml')['trainingInput']
        training_input['args'] = [
            '--gcs_csv_path', gcs_csv_path,
            '--gcs_output_path', gcs_output_path,
            '--hptune'
        ]
        job_spec = {
            'jobId': job_id,
            'trainingInput': training_input
        }

        # Launch the training job
        print(f'Launching training job for {cover_type}... ')
        launch_train_job(job_spec, config.PROJECT_ID)
        job_ids.append(job_id)

    # Wait for all jobs to finish and fetch best hyperparams
    print('Waiting for training jobs to finish...')
    opt_hyperparams = await get_opt_hyperparams(job_ids, config.PROJECT_ID)

    # Retrain using best hyperparams
    for cover_type, hyperparams in zip(cover_types, opt_hyperparams):
        gcs_csv_path = f'{gcs_run_path}/{cover_type}/raw_data.csv'
        gcs_output_path = f'{gcs_run_path}/{cover_type}/output'

        job_id = f'{run_name}_{cover_type}_opt'
        training_input = read_aip_config('config/aip_config.yaml')['trainingInput']

        # Remove hyperopt settings because we don't need to hyperopt anymore
        del training_input['hyperparameters']

        training_input['args'] = [
            '--gcs_csv_path', gcs_csv_path,
            '--gcs_output_path', gcs_output_path,
            '--n_estimators', hyperparams['n_estimators'],
            '--learning_rate', hyperparams['learning_rate'],
            '--scale_pos_weight', hyperparams['scale_pos_weight']
        ]
        job_spec = {
            'jobId': job_id,
            'trainingInput': training_input
        }

        # Launch the training job
        print(f'Launching final training job for {cover_type}... ')
        launch_train_job(job_spec, config.PROJECT_ID)
        job_ids.append(job_id)


if __name__ == '__main__':
    # Hacky way to get the command line args
    kwargs = fire.Fire(get_args)
    asyncio.run(run(**kwargs))
