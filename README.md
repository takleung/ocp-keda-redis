# (Optonal) Installation - KEDA(helm install) + Redis cluster(installed)
- KEDA_INSTANCE="keda"
- REDIS_CLUSTER_PROJECT="redis-enterprise"
- REDIS_PASSWORD=$(oc get secret redb-redb -n $REDIS_CLUSTER_PROJECT -o jsonpath='{.data.password}' | base64 --decode)
- OCP_URL="https://api.ocp-sno-aws-m7kck.sandbox2972.opentlc.com:6443"
- oc login --token=$(oc whoami -t) --server=$OCP_URL
- helm repo add kedacore https://kedacore.github.io/charts
- helm repo update
- helm install ${KEDA_INSTANCE} kedacore/keda --namespace ${KEDA_INSTANCE} --create-namespace
- oc apply -f https://raw.githubusercontent.com/takleung/ocp-keda-redis/main/redis-enterprise-scc-v2.yaml

# (Optonal) **** redis operator install, check if redis cluster healthy ****
 1. oc run redis-cli --rm -i --tty --image redis --env REDIS_PASSWORD=$REDIS_PASSWORD --env REDIS_CLUSTER_IP=$REDIS_CLUSTER_IP -- bash
 2. redis-cli -h $REDIS_CLUSTER_PROJECT -p 17750 -a $REDIS_PASSWORD
 3. set testkey testvalue
 4. get testkey
 5. return "testvalue"
 6. exit twice end of redis-cli

# (Optonal) Installation - example user workload deployment - Redis consumer
 1. sudo podman build -t takelung/redis-counter:latest .
 2. sudo podman tag takleung/redis-counter:latest docker.io/takleung/redis-counter:latest
 3. sudo podman push docker.io/takleung/redis-counter:latest

# Installation - New project, secret, triggerAuth, scaledjob
- REDIS_CLUSTER_PROJECT="redis-enterprise"
- REDIS_CLUSTER_IP=$(oc get service redb -n $REDIS_CLUSTER_PROJECT -o jsonpath='{.spec.clusterIP}')
- REDIS_PASSWORD=$(oc get secret redb-redb -n $REDIS_CLUSTER_PROJECT -o jsonpath='{.data.password}' | base64 --decode)
- CURRENT_PROJECT="keda07"
- OCP_URL="https://api.ocp-sno-aws-m7kck.sandbox2972.opentlc.com:6443"

- oc login --token=$(oc whoami -t) --server=${OCP_URL}
- oc new-project ${CURRENT_PROJECT}
- oc create secret generic redis-password -n ${CURRENT_PROJECT} --type=Opaque --from-literal=REDIS_PASSWORD=$REDIS_PASSWORD
- oc apply -f https://raw.githubusercontent.com/takleung/ocp-keda-redis/main/keda-trigger-auth-redis-secret.yaml
- curl -s https://raw.githubusercontent.com/takleung/ocp-keda-redis/main/redis-scaledjob.yaml | sed "s/10.130.0.24/$REDIS_CLUSTER_IP/g" | oc apply -f -

# Testing procedure: keda ScaledJob components Resources:
- oc run redis-cli --rm -i --tty --image redis --env REDIS_PASSWORD=$REDIS_PASSWORD --env REDIS_CLUSTER_IP=$REDIS_CLUSTER_IP -- bash 
- for i in {1..5}
   do
      redis-cli -h $REDIS_CLUSTER_IP -p 17750 -a $REDIS_PASSWORD LPUSH mylist item1 item2 item3 item4 item5
   done
<-- You should see the scaledJob has been triggered.

# Clean up data
- redis-cli -h $REDIS_CLUSTER_IP -p 17750 -a $REDIS_PASSWORD DEL mylist
- oc delete project $CURRENT_PROJECT

# Useful commands
- oc run redis-cli --rm -i --tty --image redis -- bash
- redis-cli -h $REDIS_CLUSTER_IP -p 17750 -a $REDIS_PASSWORD
- set testkey testvalue
- get testkey
- redis-cli -h 10.130.0.24 -p 17750 -a $REDIS_PASSWORD LPUSH mylist item1 item2 item3 item4 item5
- redis-cli -h 10.130.0.24 -p 17750 -a $REDIS_PASSWORD LLEN mylist
- redis-cli -h 10.130.0.24 -p 17750 -a $REDIS_PASSWORD DEL mylist
- oc logs -f $(oc get pods -n keda | grep keda-operator | grep -v metrics-apiserver | awk '{print $1}') -n keda







