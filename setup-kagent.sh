#!/bin/bash

k3d cluster create my-cluster \
    --api-port 6443 \
    --k3s-arg "--disable=traefik@server:0" \
    --registry-create my-cluster-registry:0.0.0.0:5010

kagent install --namespace kagent --profile minimal


