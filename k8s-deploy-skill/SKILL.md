---
name: Kubernetes Simple Deploy
description: Assists with deploying simple apps to Kubernetes, explaining manifests, deployments and services for beginners.
---

# Kubernetes simple deploy skill

Use this skill when users want to deploy a basic app on the Kubernetes cluster.

## How It Actually Works

1. You tell me: app name, image, and optionally number of replicas and port.
2. I **call the tool** `deploy-app.py` with your parameters.
3. The **script** (not me) generates a correct two-resource manifest (Deployment + Service) and writes it to `temp-manifest.yaml`.
4. The **agent** is expected to run `kubectl apply -f temp-manifest.yaml` against the current Kubernetes context.

## Example

```text
User: Deploy an app called "nginx" using image "docker/nginx" with 2 replicas on port 8080.

Agent: Calls deploy-app.py nginx docker/nginx 2 8080
→ Creates/updates Deployment + Service in one shot
Agent in turn applies the generated temp-manifest.yaml to the cluster
```
