PROJECT_ID="gothic-parsec-308513"

# Make sure client libraries can authenticate
gcloud auth application-default login

# Make sure we are working in the correct project
gcloud config set project $PROJECT_ID

# Enable necessary services, this can also be done using Cloud console
gcloud services enable \
cloudbuild.googleapis.com \
container.googleapis.com \
cloudresourcemanager.googleapis.com \
iam.googleapis.com \
containerregistry.googleapis.com \
containeranalysis.googleapis.com \
ml.googleapis.com \
dataflow.googleapis.com 

#The Cloud Build service account needs the Editor permissions in your GCP project
#to upload the pipeline package to an AI Platform Pipelines instance.
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
CLOUD_BUILD_SERVICE_ACCOUNT="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:$CLOUD_BUILD_SERVICE_ACCOUNT \
  --role roles/editor
