
# instructions

## prerequisites

- docker
- k3d
- kagent cli

## setup

create a cluster with a local registry, and install kagent:

```shell
./setup-kagent.sh
```

build (and push) the k8s-deploy-skill:

```shell
pushd k8s-deploy-skill
./build-image.sh
popd
```

define a the simple k8s agent:

```shell
k apply -f simple-k8s-agent.yaml
```
