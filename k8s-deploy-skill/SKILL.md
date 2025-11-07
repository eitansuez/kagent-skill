---
name: Kubernetes Simple Deploy
description: Assists with deploying simple apps to Kubernetes consisting of a deployment and a service.
---

# Kubernetes simple deploy skill

Use this skill when users want to deploy a basic app on the Kubernetes cluster.

## How It Actually Works

1. User requests an app be deployed, and supplies a name, an image, and optionally number of replicas and a port.
2. The script `scripts/deploy-app.py` should be called with these parameters.
3. The **script** generates a correct two-resource manifest (Deployment + Service) and writes it to the file `temp-manifest.yaml`.
4. The **agent** is expected to run `kubectl apply -f temp-manifest.yaml` against the current Kubernetes context.

## Example

```text
User: Deploy an app called "nginx" using image "docker/nginx" with 2 replicas on port 8080.

Agent: Calls deploy-app.py nginx docker/nginx 2 8080
The "skill" creates a manifest named temp-manifest.yaml consisting of a Deployment + Service in one shot
The Agent in turn applies the generated temp-manifest.yaml to the cluster
```
