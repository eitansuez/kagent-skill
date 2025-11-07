#!/usr/bin/env python3

# deploy-app.py

import sys
from pathlib import Path
from textwrap import dedent

def generate_manifest(app_name, image, replicas=1, port=80):
    """Generate valid Kubernetes YAML using only built-in Python"""
    
    manifest = f"""\
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: {app_name}
          labels:
            app: {app_name}
        spec:
          replicas: {replicas}
          selector:
            matchLabels:
              app: {app_name}
          template:
            metadata:
              labels:
                app: {app_name}
            spec:
              containers:
              - name: {app_name}
                image: {image}
                ports:
                - containerPort: {port}
        ---
        apiVersion: v1
        kind: Service
        metadata:
          name: {app_name}-svc
          labels:
            app: {app_name}
        spec:
          type: LoadBalancer
          selector:
            app: {app_name}
          ports:
          - port: 80
            targetPort: {port}
            protocol: TCP
        """

    # Clean dedent + write
    clean_yaml = dedent(manifest).strip() + "\n"
    file_path = Path("temp-manifest.yaml")
    file_path.write_text(clean_yaml, encoding="utf-8")
    return str(file_path)


def print_usage():
    print("""Kubernetes Zero-Dependency Deploy

Usage:
  python deploy-app.py <name> <image> [replicas] [port]

Examples:
  python deploy-app.py web nginx:latest
  python deploy-app.py api ghcr.io/myorg/api:v2 3 5000
  python deploy-app.py redis redis:7.2 1 6379

No pip, no yaml, no problem.
""")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or "-h" in args or "--help" in args:
        print_usage()
        sys.exit(0)

    if len(args) < 2:
        print("Error: Need <name> <image>")
        print_usage()
        sys.exit(1)

    app_name = args[0]
    image = args[1]
    replicas = 1
    port = 80

    # Safely parse optional numeric args
    for arg in args[2:]:
        if arg.lstrip("-").isdigit():
            num = int(arg)
            if replicas == 1:
                replicas = num
            elif port == 80:
                port = num

    print(f"Deploying {app_name}")
    print(f"   Image: {image}")
    print(f"   Replicas: {replicas}")
    print(f"   Container port: {port} → Service port: 80")
    print()

    path = generate_manifest(app_name, image, replicas, port)
    print(f"Manifest saved → {path}")
    print()
    print("Next:")
    print(f"   kubectl apply -f {path}")
