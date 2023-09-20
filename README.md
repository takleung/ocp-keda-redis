# ocp-keda-redis
Installation
- keda helm
    - helm repo add kedacore https://kedacore.github.io/charts
    - helm repo update
    - helm install keda kedacore/keda --namespace keda --create-namespace
- add scc --> oc apply -f redis-enterprise-scc-v2.yaml
- Redis enterprise, 3 worker nodes by default
    - Operator (certifed)
    - Expose rec-ui passthru
    - Console login info, secret rec
- add redis secret --> oc apply -f redis-password.yaml
- add trigger auth --> oc apply -f keda-trigger-auth-redis-secret.yaml (tried to plain text password not working)
- add keda config --> redis-scaleobject.yaml (leverage HorizontalPodAutoscalers, auto gen)

Redis consumer
- sudo podman build -t takelung/redis-counter:latest .
- sudo podman tag takleung/redis-counter:latest docker.io/takleung/redis-counter:latest
- sudo podman push docker.io/takleung/redis-counter:latest

Testing procedure: keda ScaledJob components
Resources:
- keda --> all components except redis cluster
- redis-enterprise --> redis cluster
- ScaledJob --> redis-scaledjob
Steps:
- oc login
- oc project keda
- oc run redis-cli --rm -i --tty --image redis -- bash
- redis-cli -h 10.130.0.24 -p 17750 -a uZTbwJVn LPUSH mylist item1 item2 item3 item4 item5
You should see the scaledJob has been triggered.

Useful commands
- oc run redis-cli --rm -i --tty --image redis -- bash
- redis-cli -h 10.130.0.24 -p 17750 -a uZTbwJVn
- set testkey testvalue
- get testkey
- redis-cli -h 10.130.0.24 -p 17750 -a uZTbwJVn LPUSH mylist item1 item2 item3 item4 item5
- redis-cli -h 10.130.0.24 -p 17750 -a uZTbwJVn LLEN mylist
- redis-cli -h 10.130.0.24 -p 17750 -a uZTbwJVn DEL mylist
- oc logs -f keda-operator-596964bcb-tr6dh


