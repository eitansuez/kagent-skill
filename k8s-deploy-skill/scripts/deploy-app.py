#!/usr/bin/env python3

# deploy-app.py
# Kubernetes Simple Deploy Skill — one-tool manifest generator
# Works perfectly with minikube, kind, k3d — zero YAML editing required

import yaml
import sys
from pathlib import Path

def generate_manifest(app_name, image, replicas=1, port=80):
    """Create Deployment + Service manifest and write to temp-manifest.yaml"""
    deployment = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {'name': app_name},
        'spec': {
            'replicas': int(replicas),
            'selector': {'matchLabels': {'app': app_name}},
            'template': {
                'metadata': {'labels': {'app': app_name}},
                'spec': {
                    'containers': [{
                        'name': app_name,
                        'image': image,
                        'ports': [{'containerPort': int(port)}]
                    }]
                }
            }
        }
    }

    service = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {'name': app_name},
        'spec': {
            'selector': {'app': app_name},
            'ports': [{'port': 80, 'targetPort': int(port)}],
            'type': 'LoadBalancer'  # minikube service --url works out of the box
        }
    }

    full_yaml = yaml.dump(deployment, sort_keys=False) + "---\n" + yaml.dump(service, sort_keys=False)
    file_path = Path('temp-manifest.yaml')
    file_path.write_text(full_yaml)
    return str(file_path)

def print_usage():
    print("""Kubernetes Quick Deploy Tool

Usage:
  python deploy-app.py <name> <image> [replicas] [port]

Examples:
  python deploy-app.py hello nginx:latest
  python deploy-app.py api myreg/backend:v2 5 5000
  python deploy-app.py redis redis:7.2 2 6379
  python deploy-app.py vote docker/example-voting-app 4 8080

Defaults: replicas=1, port=80 → Service exposes on http://.../:80
""")

if __name__ == '__main__':
    if len(sys.argv) < 3 or '-h' in sys.argv or '--help' in sys.argv:
        print_usage()
        sys.exit(0 if '-h' in sys.argv or '--help' in sys.argv else 1)

    app_name = sys.argv[1]
    image    = sys.argv[2]
    replicas = int(sys.argv[3]) if len(sys.argv) >= 4 and sys.argv[3].isdigit() else 1
    port     = int(sys.argv[4]) if len(sys.argv) >= 5 and sys.argv[4].isdigit() else 80

    if len(sys.argv) >= 4 and not sys.argv[3].isdigit():
        print(f"Warning: replicas '{sys.argv[3]}' not integer → using 1")
    if len(sys.argv) >= 5 and not sys.argv[4].isdigit():
        print(f"Warning: port '{sys.argv[4]}' not integer → using 80")

    print(f"Deploying: {app_name} → {image} | {replicas} replica(s) | port {port}")

    generate_manifest(app_name, image, replicas, port)

    print("\nNext steps:")
    print(f"  kubectl apply -f temp-manifest.yaml")
    print(f"  kubectl get pods -l app={app_name}")
    print(f"  kubectl get svc {app_name}")
    print(f"  minikube service {app_name} --url")
    print(f"  curl $(minikube service {app_name} --url --format '{{{{.}}}}}')")
