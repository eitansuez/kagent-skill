#!/bin/bash

k3d registry create myreg --port 127.0.0.1:5001
docker network connect k3d-my-cluster k3d-myreg || true
k3d cluster create my-cluster \
  --registry-use k3d-myreg:5001 \
  --registry-config "$PWD/registries.yaml"

kagent install --namespace kagent --profile minimal


