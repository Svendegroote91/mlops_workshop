"""Deploy KFP pipeline to KFP host."""
import tempfile

import fire
import kfp

from pipelines.end_to_end_pipeline import end_to_end_pipeline


# The URL of the Kubeflow Pipelines Host (can be found in the AI platform pipelines UI)
KFP_HOST = 'YOUR-KFP-HOST'
KFP_CLIENT = kfp.Client(KFP_HOST)

PIPELINES = {
    'end_to_end_pipeline': end_to_end_pipeline
}


def deploy_pipeline(identifier, pipeline_name):
    pipeline_id_name = identifier + "-" + pipeline_name
    pipeline_id = KFP_CLIENT.get_pipeline_id(pipeline_id_name)
    pipeline_function = PIPELINES[pipeline_name]

    if pipeline_id:
        print('Pipeline already exists, deleting it first...')
        KFP_CLIENT.delete_pipeline(pipeline_id)

    with tempfile.NamedTemporaryFile() as temp_f:
        pipeline_filename = f'{temp_f.name}.tar.gz'
        kfp.compiler.Compiler().compile(pipeline_function, pipeline_filename)
        KFP_CLIENT.upload_pipeline(
            pipeline_filename, pipeline_id_name,
            description='Some descriptive description...'
        )
        print('Successfully deployed', pipeline_name)


if __name__ == '__main__':
    fire.Fire(deploy_pipeline)
