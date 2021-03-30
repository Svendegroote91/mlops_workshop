"""Run KFP pipeline."""

import fire
import kfp


# The URL of the Kubeflow Pipelines Host (can be found in the AI platform pipelines UI)
KFP_HOST = 'https://1cad5bb08a32308d-dot-europe-west1.pipelines.googleusercontent.com'
KFP_CLIENT = kfp.Client(KFP_HOST)


def run_pipeline(job_name, identifier, pipeline_name, experiment_name='Default'):
    # Only required parameters is gcs_bucket, the rest has default values
    pipeline_id_name = identifier + "-" + pipeline_name
    run_params = {
        'gcs_bucket': 'mlops-workshop-unilin'
    }

    try:
        experiment_id = KFP_CLIENT.get_experiment(experiment_name=experiment_name).id
    except ValueError:
        experiment_id = KFP_CLIENT.create_experiment(experiment_name).id

    try:
        pipeline_id = KFP_CLIENT.get_pipeline_id(pipeline_id_name)

        KFP_CLIENT.run_pipeline(
            experiment_id, job_name=job_name,
            params=run_params, pipeline_id=pipeline_id
        )

    except Exception as exc:
        print('Failed to run pipeline:', exc)
        exit(1)


if __name__ == '__main__':
    fire.Fire(run_pipeline)
