#!/bin/bash

k3d cluster create my-cluster --registry-create my-cluster-registry:0.0.0.0:5010

kagent install --namespace kagent --profile minimal


