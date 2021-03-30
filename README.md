# MLOps Workshop

This folder contains all the code for the MLOps ML in production workshop on Thursday.
As mentioned before, it still needs to be adapted in some places, but the general structure is already there and both parts should already run successfully.  

The `setup_bq.sh` and `setup.sh` files are to load the toy dataset in BigQuery and that all necessary services are activated. This is something that only needs to be run once, so you don't need to run it again.   

Two commands that are useful though:
- `gcloud auth application-default login` - This command will cause a browser window to pop up and ask you to login using you google account. It then sets the necessary variables to make sure all client libraries are able to connect to GCP.
- `gcloud config set project $PROJECT_ID` - This command sets the default project to be used.  

The ai_platform_training folder contains all the code for the first part of the hands-on session. It illustrates how to using AI Platform Training to launch a hyperparameter optimization job.   

The kfp folder contains all the code for the second part of the hands-on session. It illustrates how to take the steps from the previous example and make them into clean reusable components. Some changes need to be made to the implementation of the logic of each step, mainly having to do with saving and loading data to and from Cloud Storage at the end and start of each step.   

## Pre-requisites

* [gcloud SDK](https://cloud.google.com/sdk/docs/install)
* [kubectl](https://cloud.google.com/sdk/docs/install)