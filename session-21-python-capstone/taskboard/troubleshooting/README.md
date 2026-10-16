# Troubleshooting lab

Two deliberately broken manifests. Apply one, investigate with the Session 14 ladder (`get`, `describe`, `events`, `logs`), fix it, verify.

| File | What is wrong | Symptom | Fix |
| --- | --- | --- | --- |
| `broken-image.yaml` | Image tag `does-not-exist` | Pod stuck in `ErrImagePull` / `ImagePullBackOff` | `kubectl set image deployment/taskboard-broken-image backend=taskboard-backend:local -n taskboard` |
| `broken-service.yaml` | Selector `app: label-that-does-not-exist` | Service has no endpoints, connections time out | `kubectl patch svc broken-service -n taskboard -p '{"spec":{"selector":{"app":"taskboard-backend"}}}'` |

```bash
kubectl apply -f troubleshooting/broken-image.yaml
kubectl get pods -n taskboard -l app=broken-image
kubectl describe pod -n taskboard -l app=broken-image | tail -12
kubectl get events -n taskboard --sort-by=.lastTimestamp | tail -5

kubectl apply -f troubleshooting/broken-service.yaml
kubectl get svc,endpoints broken-service -n taskboard
kubectl get pods -n taskboard --show-labels
```
