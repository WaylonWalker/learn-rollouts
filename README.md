# Learn Rollouts

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

``` bash
# access the argocd server
kubectl port-forward service/argo-argocd-server -n argocd 8080:443
argocd admin initial-password -n argocd
argocd login localhost:8080
```

``` bash
argocd account update-password --account admin --new-password password
argocd app list
argocd app create apps --repo https://github.com/waylonwalker/learn-rollouts --path apps --dest-server https://kubernetes.default.svc --dest-namespace argocd
argocd app list
argocd app sync apps
argocd app list
```
