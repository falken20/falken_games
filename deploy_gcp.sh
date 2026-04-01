#!/usr/bin/env bash

set -euo pipefail

PROJECT_ID="falken-games"
REGION="${REGION:-europe-west1}"

gcloud config set project "$PROJECT_ID"
gcloud builds submit --config cloudbuild.yaml --substitutions=_REGION="$REGION"