### Tech-Stack:

```
python3.9 | flask
```

#### *Run all commands in root project dir*

## Docker Build
### Build Docker Container:

```
docker build --tag python-docker .
```

### Run Docker Container:

```
docker run python-docker
```


## Install Locally
### Install from requirements
```
python3 -m pip install -r requirements.txt
```

### Run tests
```
python3 -m pytest
```

### API URL / Port:

```
http://127.0.0.1:5000/api/ping
http://127.0.0.1:5000/api/posts
```