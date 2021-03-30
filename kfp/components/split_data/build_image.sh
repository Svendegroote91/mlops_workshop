# Set global variables
REGION="europe-west1"
PROJECT_ID="gothic-parsec-308513"

# Build trainer image
IMAGE_NAME="split_data"
IMAGE_TAG="latest"
IMAGE_URI="eu.gcr.io/$PROJECT_ID/$NAME/$IMAGE_NAME:$IMAGE_TAG"
gcloud builds submit --tag $IMAGE_URI $IMAGE_NAME