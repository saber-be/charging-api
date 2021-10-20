# Challenge 1: API Service
## Install on local
1- Install dependencies

```
pip install -r requirements.txt
```

2- Start service

```
uvicorn service.main:app --host 0.0.0.0 --port 8000
```
3- Go to http://0.0.0.0:8000

## Run on docker
1- Build docker image

```
docker build -t imagename .
```

2- Run container
```
docker run --name containername -p 8000:80 -d imagename
```

3- Go to http://0.0.0.0:8000

## Run Test cases
Run `pytest` in project directory

```
pytest
```

# Challenge 2: Suggest improvements to the API design

## Suggestion 1:
There's no need to send Rate info in API requests, it’s better to get Rate info from the DB server.
If there are different rates based on locations(state/city/etc), we can put the location id in API and get the related Rate from the DB server.

### Advantages:
- Rate's logic (say: set the rates of Energy, Time, etc.) will deploy on the backend and increase flexibility and security.
### Disadvantages:
- Need to query rates from DB, it has both time and money costs, but using cache could reduce these costs.
## Suggestion 2:
let's assume the internet connection is always good(as a developer from Iran, this is impossible), by this assumption, there's no need to send timestamps to the server and we can send one request to the server for each charge event(start/end transaction) and use server time as timestamps.

### Advantages:
- Timestamps are more reliable (in fact every data that comes from the client aren’t reliable)
- The server could have more control over the charging process.
  - Ex 1: After receiving the start transactions request, it can review the user’s credit and decide whether to allow the user to start charging.
  - Ex 2: If there is any problem on the server or in communication between client and server the start transaction request will fail and the charging process will not start, that is a good protection mechanism.

### Disadvantages:
- The number of requests to the server will be double.
- The server needs to store start transaction event info somewhere and retrieve it after receiving the end transaction event and then complete the charging process.


