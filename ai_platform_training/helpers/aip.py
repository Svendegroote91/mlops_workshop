"""AI Platform related helpers."""

import asyncio
import time
import yaml

from googleapiclient import discovery
from googleapiclient import errors

# The discovery module is a wrapper around the raw GCP http APIs
CLOUDML = discovery.build('ml', 'v1')


def launch_train_job(job_spec, project_id):
    try:
        full_project_id = f'projects/{project_id}'
        # This calls the projects.jobs.create method of the AI Platform Training API
        # See: https://cloud.google.com/ai-platform/training/docs/reference/rest/v1/projects.jobs/create
        request = CLOUDML.projects().jobs().create(body=job_spec, parent=full_project_id)
        response = request.execute()
        print(f'\tJob is {response["state"]}')
    except errors.HttpError as err:
        print('There was an error launching the training job. Check the details:')
        print(err._get_reason())


def read_aip_config(config_yaml):
    with open(config_yaml) as f:
        aip_config = yaml.safe_load(f)

    return aip_config


async def wait_for_train_job(job_id, project_id, interval, timeout):
    done = False

    start = time.time()
    while not done:
        try:
            full_job_id = 'projects/{}/jobs/{}'.format(project_id, job_id)
            request = CLOUDML.projects().jobs().get(name=full_job_id)
            response = request.execute()

            if response['state'] in ('SUCCEEDED', 'FAILED', 'CANCELLED'):
                done = True
            elif time.time() - start >= timeout:
                print('Operation timed out.')
                done = True
            else:
                await asyncio.sleep(interval)
        except errors.HttpError as err:
            print(err)
        except Exception as err:
            print(err)
            print("Unexpected error")

    if response['state'] != 'SUCCEEDED':
        print(f'Training job {job_id} failed. See job details for more info.')
    else:
        print(f'Training job {job_id} succeeded.')

    return response['trainingOutput']


async def get_opt_hyperparams(job_ids, project_id, interval=15, timeout=7200):
    training_outputs = await asyncio.gather(*[wait_for_train_job(job_id, project_id, interval, timeout)
                                              for job_id in job_ids])

    opt_hyperparams = [to['trials'][0]['hyperparameters'] for to in training_outputs]

    return opt_hyperparams
