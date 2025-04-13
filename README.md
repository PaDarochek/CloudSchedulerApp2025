# Scheduler app

Scheduler app helps you to sort and prioritize you tasks within time interval based on deadline and percentage of completion.

# Launching scheduler app via minikube

Build docker:

    $ docker build -t scheduler .

Start and configure minikube:

    $ minikube start
    $ eval $(minikube -p minikube docker-env)
    $ kubectl apply -f ./k8s_config.yml

Check minikube IP:

    $ minikube ip
    192.168.49.2

Check API port (take 2nd value from `PORT` section of `scheduler` service):

    $ kubectl get svc
    NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
    kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP          6m21s
    redis        ClusterIP   10.96.40.156     <none>        6379/TCP         6m18s
    scheduler    NodePort    10.100.162.213   <none>        5000:32491/TCP   6m18s

In above example API is available on `http://192.168.49.2:32491/`

# Using API

## Add task

To add task with parameters `title`, `deadline`, `created_date`, `plan` (amount of time planned for task completion) and `work` (amount of time already spent on task completion) use curl request:

    $ curl -X POST http://127.0.0.1:5000/task\?title\=print\&deadline\=10-04-2025\&created_date\=09-04-2025\&plan\=3\&work\=1

## Get tasks list

To get list of all tasks use browser request:

    $ http://192.168.49.2:32491/list

## Get sorted tasks list

To sort tasks relevant to `start_date` - `end_date` time interval use browser request with parameters:

    $ http://192.168.49.2:32491/sort?start_date=07-04-2025&end_date=12-04-2025
