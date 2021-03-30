# MLOps workshop hands-on session 1: AI Platform training

The goal of this first hands-on session is to provide an example of how AI platform training can be used to train a number of models in parallel and how to configure the hyperparameter tuning functionality. The dataset that is used is the [Covertype dataset](https://archive.ics.uci.edu/ml/datasets/covertype), where the goal is to predict forest cover type (7 categories) from cartographic variables.


A number of very basic ML pipeline steps have already been implemented and can be found in the `steps` folder. These steps are the following:

1) Prepare the datasets: The purpose of this step is to prepare a number of datasets that can be used in the rest of the pipeline. This preparation step will create 1 dataset for each cover type (so 7 datasets in total), where the goal is binary classification of whether an input sample belongs to this cover type or not. The data is read from BigQuery and the resulting datasets are stored in a Google Cloud Storage (GCS) bucket.

2) Split the data: In this step, the input dataset is split into a training and a test set.

3) Preprocessing: Here a very basic sklearn preprocessor is fit that will be used for preprocessing train and test data.

4) Train: An XGboost model is trained and a small number of hyperparameters can be selected.

5) Evaluate: In this final step, the trained model is evaluated (accuracy and f1-score) on the test set.

These basic steps are brought together in the `python train_evaluate.py` script, which runs all these steps and finally prints the evaluation metrics.  

## Running locally
In order to run the training locally, you can simply run `python run_local.py`. This script will prepare the datasets and then run the training and evaluation for each different cover type (without hyperparameter tuning). The resulting models (preprocessor and xgboost) are stored in a GCS bucket to allow later reuse.   
The command to use in the workshop is: `python run_local.py mlops-workshop-unilin [YOUR-NAME]`

## Running on AI Platform
Training locally is fine for a small number of models and smaller datasets but can take a long time otherwise. The `run_aip.py` script shows how you can submit multiple AI Platform Training jobs in parallel, to cut down on the total training time and it also includes hyperparameter tuning for the best results.  

### Creating a custom Docker container
In order to be able to run the training job on AI platform, we first need to prepare the custom Docker container implementing the training logic. We can simply reuse the `train_evaluate.py` script from before. In the Dockerfile we start from the desired Python version, install the dependencies and copy the necessary source code files over to the container. Finally, we tell the container to run the `train_evaluate.py` script when it is started. The `build_trainer_image.sh` script uses Cloud Build to build this Docker container, which will also result in the image being readily available in Google Container Registry (GCR).  
Once this container has been built, we are ready to submit the training job. This can be done using the `gcloud` CLI or using the Python interface as illustrated in the `run_aip.py` script. In `config/aip_config.yaml` you can see the AI Platform Training configuration (note here that we use the GCR URI from the previously built trainer image). The specifics of the training job are defined here.   
The script will first launch a hyperparameter optimisation job for each cover type, then wait until all jobs are finished and then launch a final training job for each cover type with the optimal hyperparameters.  

The command to use in the workshop is: `python run_aip.py gothic-parsec-308513 [YOUR-NAME]`  
