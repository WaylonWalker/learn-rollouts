# Learn Rollouts

An argocd app of apps that shows how to use rollouts.

## hello-world application

This application consists of a flask application in `/hello-world`, it has 3
different versions that you can play with tagged `v1`, `v2`, and `v3`.  It will
respond with a different version number based on the version that is active.

When rolled out with the provided kind cluster it will respond with a different
header color based on the environment that it is running in.  Since the idea of
rollouts is zero downtime and to rollout the exact same application both in
preview and active, the only difference is the url that it is deployed on.
Based on this url flask will choose the header color.

* active: blue
* preview: pink
* local: green
* unknown: tan

### Docker images

Docker images have been pushed to a public docker hub so they are easily accessible.

<https://hub.docker.com/r/waylonwalker/learn-rollouts/tags>

## Example

Here you can see the application running in all 3 states, active, preview, and local.

![image](https://github.com/WaylonWalker/learn-rollouts/assets/22648375/c0355d25-1e9b-4ef4-8eb5-ed6c6a9e7ce4)

## app of apps

This application is setup as an app of apps.  You will deploy the first application and argocd will manage that app as well as the rest.

![image](https://github.com/WaylonWalker/learn-rollouts/assets/22648375/b5fcdec7-1042-4393-8a9f-9339822a5c6d)

From left to right in the image there is the apps application that contains all
of the argocd applications, hello-world (the flask application) and argo
rollouts..

## Setup

I have given instructions for this entire project to run in a
[kind-cluster](https://kind.sigs.k8s.io/docs/user/quick-start/).  First we are
going to spin up the kind cluster, install argocd and deploy the app of apps.

First fork the repo, and change the repoURL in `apps/apps.yaml` to your own repoURL.

``` bash
kind create cluster --name rollout --config kind-config.yaml
# your first time through you need to add the argocd repo
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
# install argocd into the cluster
helm install argo argo/argo-cd --namespace argocd --create-namespace
# deploy the app of apps
kubectl apply -f apps/apps.yaml
```

Now we can access the argocd server by first forwarding the port, getting the
initial password, then logging in to the `admin` account with that password.

``` bash
# access the argocd server
kubectl port-forward service/argo-argocd-server -n argocd 8080:443
argocd admin initial-password -n argocd
argocd login localhost:8080
# you can also access it through a web browser at https://localhost:8080
# you will have to accept the certificate the first time
```

Now we can refresh each of our apps with the web browser, or the cli.

``` bash
argocd app list
```

```
NAME                CLUSTER                         NAMESPACE      PROJECT  STATUS     HEALTH     SYNCPOLICY  CONDITIONS                  REPO                                            PATH                     TARGET
argocd/apps         https://kubernetes.default.svc  argo           default  OutOfSync  Healthy    Auto-Prune  SyncError                   https://github.com/waylonwalker/learn-rollouts  apps                     HEAD
argocd/hello-world  https://kubernetes.default.svc  hello-world    default  Synced     Suspended  Auto-Prune  RepeatedResourceWarning(2)  https://github.com/waylonwalker/learn-rollouts  hello-world/deployments  HEAD
argocd/rollouts     https://kubernetes.default.svc  argo-rollouts  default  Synced     Healthy    Auto-Prune  <none>                      https://github.com/waylonwalker/learn-rollouts  rollouts-app             HEAD
```

``` bash
argocd app sync apps
argocd app sync rollouts
argocd app sync hello-world
```

If you wish to update the argo-server password you can use the following command:

``` bash
argocd account update-password --account admin --new-password password
```

## Rollouts

install the rollouts plugin with the instructions from the
[installation](https://argoproj.github.io/argo-rollouts/installation/#kubectl-plugin-installation)
page. Then we can access the rollouts dashboard.

``` bash
kubectl argo rollouts dashboard
```

![image](https://github.com/WaylonWalker/learn-rollouts/assets/22648375/6030a889-99fa-4d21-95cc-3a630a225af5)

we can also access rollouts through the kubectl plugin.

``` bash
kubectl argo rollouts get rollout hello-world-bluegreen -n hello-world --watch
```

## Rolling out a new version

To roll out a new version of the hello-world application we can bump the
container tag from `v1` to `v2` by updating the deployment.yaml file in the
`hello-world/deployments` directory. Pushing that change, then we can `argocd app sync`.

<https://github.com/WaylonWalker/learn-rollouts/blob/main/hello-world/deployments/deployment.yaml#L31>

You can now play with changing between different tags, and see how the rollout
goes.  active is hosted at localhost:30001 and preview at localhost:30002.
