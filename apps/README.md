# Hello World

## Api


"Hello World" application that exposes the following

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

Note: Use database is in memory.

## Docker
App:
```sh
docker run -d -p 8000:8000 python
docker build -t python .

```
## Test
```sh
docker run -it myapp pytest

```

## Image Registry

```sh
kubectl create secret docker-registry ghcr-login-secret --docker-server=https://ghcr.io --docker-username=USERGITHUB --docker-password=ghp_TEMPTOKEN --docker-email=USER@github.com
```
## HELM COMFIG

For deploy locally need build each dockerfile separate.

Added chart folder with custom values.yaml

In path ./example/apps/charts run:

```sh
helm upgrade -f ../python/hello-world/values.yaml python ./
```
## Tests Curls
```sh
curl http://localhost:8000/hello/john
```
* Replace localhost with terraform output ALB url
```sh
curl -X PUT -H "Content-Type: application/json" -d '{"dateOfBirth": "1990-01-22"}' http://localhost:8000/hello/john
```
```sh
curl http://localhost:8000/hello/john
```
