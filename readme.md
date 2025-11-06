
# basic setup instructions

## prerequisites

docker
k3d
kagent cli

## setup

create a cluster with a local registry, and install kagent:

```shell
./setup-kagent.sh
```

define a the simple k8s agent:

```shell
k apply -f simple-k8s-agent.yaml
```
