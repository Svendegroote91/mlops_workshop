# Allow caching in Cloud Build, which can greatly speed them up
# See: https://cloud.google.com/cloud-build/docs/speeding-up-builds
gcloud config set builds/use_kaniko True

bash prepare_datasets/build_image.sh
bash split_data/build_image.sh
bash preprocessing/build_image.sh
bash training/build_image.sh
bash evaluation/build_image.sh
