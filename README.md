<h1>API Service</h1>

<h2>Install on local</h2>
1- Install dependencies

```
pip install -r requirements.txt
```

2- Start service

```
uvicorn service.main:app --host 0.0.0.0 --port 8000 
```
3- Go to http://0.0.0.0:8000/docs

<h2>Run on docker</h2>
1- Build docker image

```
docker build -t imagename .
```

2- Run container
```
docker run --name containername -p 8000:80 -d imagename
```

3- Go to http://0.0.0.0:8000/docs
