# devops-sample-apps

## Api


Design and code a simple "Hello World" application that exposes the following

HTTP-based APIs:
Description: Saves/updates the given user’s name and date of birth in the database.
Request: PUT /hello/<username> { “dateOfBirth”: “YYYY-MM-DD” }
Response: 204 No Content
Note:
<username> must contain only letters.
YYYY-MM-DD must be a date before the today date.
Description: Returns hello birthday message for the given user
Request: Get /hello/<username>
Response: 200 OK

Response Examples:
A. If username’s birthday is in N days:
{ “message”: “Hello, <username>! Your birthday is in N day(s)”
}
B. If username’s birthday is today:
{ “message”: “Hello, <username>! Happy birthday!” }
Note: Use storage/database of your choice.




## Image Registry

```
kubectl create secret docker-registry ghcr-login-secret --docker-server=https://ghcr.io --docker-username=cifuab --docker-password=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 --docker-email=cifuab@gmail.com
```
## HELM COMFIG

For deploy localy need build each dockerfile separate.

Added chart folder with custom values.yaml

In path ./example/apps/charts run:

```
helm upgrade -f ../java/hello-world/values.yaml go ./

```
## Config nginx-igress

In bash execute

```
cat <<EOF | kubectl apply -f -
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: api
  annotations:
    nginx.org/rewrites: "serviceName=go rewrite=/api/;serviceName=java rewrite=/api/"
spec:
  rules:
   - http:
      paths:
      - path: /api/v1/
        backend:
          serviceName: go
          servicePort: 80

EOF
```

kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://api.local/v2:80; done"

```
---
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-app-ingress
  namespace: default
  labels:
    app: api-app
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/healthcheck-protocol: HTTP
    alb.ingress.kubernetes.io/healthcheck-port: traffic-port
    alb.ingress.kubernetes.io/healthcheck-interval-seconds: '15'
    alb.ingress.kubernetes.io/healthcheck-timeout-seconds: '5'
    alb.ingress.kubernetes.io/success-codes: '200'
    alb.ingress.kubernetes.io/healthy-threshold-count: '2'
    alb.ingress.kubernetes.io/unhealthy-threshold-count: '2'
spec:
  rules:
    - http:
        paths:
          - path: /api/v1
            pathType: Prefix
            backend:
              service:
                name: go
                port:
                  number: 80                        
EOF
´´´