# Movie list app

Simple movie app list application with edit, add, and delete functions.
Built with Python using Flask, WTF-forms, and SQLAlchemy. Uses SQLite DB to
store all the added movies. The list will automatically
sort all the movies based on the rating you gave them,
from lowest to highest

![demo-gif](https://github.com/saymolet/ml-flask/blob/main/img/ml-flask-demo.gif)



## Prerequisites
### Local build:
* Python 3.10 and up

* Install all needed dependencies:
```commandline
pip install -r requirements.txt
```
* API Key. Register at `https://www.themoviedb.org/`. 
Go to `Profile --> Settings --> API` and in the `API Key (v3 auth)` 
section copy your own API key. It should look something like
this "`8eba9165bc57j105827ff2df47879265`". Replace `{YOUR_API_KEY}`
in commands with your own API Key. Example:
```commandline
export API_KEY=8eba9165bc57j105827ff2df47879265
```

### Run inside the docker container:
* Docker
* API Key (see above for instructions)

## Usage
### Local build
Export your own API Key as an environmental variable:
```commandline
export API_KEY={YOUR_API_KEY}
```
Run the application locally:
```commandline
python -m flask run
```
You can access the application on `127.0.0.1:5000`

### Run inside the docker container with named volumes
Build the docker image:
```commandline
docker build -t ml-app-flask .
```

Run the docker container
```commandline
docker run -d -p 5000:5000 -e API_KEY={YOUR_API_KEY} -v dbvolume:/usr/app/instance ml-app-flask
```
You can access the application on `127.0.0.1:5000`

## CI/CD Pipeline

### Prerequisites
* [Docker-in-docker Jenkins](https://www.jenkins.io/doc/book/installing/docker/)
* AWS EC2 Instance
* API Key exported on EC2 instance (write to .bashrc)
* Fine-grained personal access token for GitHub
* Python 3.10 with pip and poetry dependency manager inside Jenkins container
* SSH Agent plugin for Jenkins
* Credentials configured on Jenkins

Jenkins file uses a [shared library](https://gitlab.com/saymolet/jenkins-shared-library.git) of my own.
You can tweak or change any part of the Jenkins file as needed for your own needs.

This pipeline automatically, on every commit, 
increments the version of the app in the pyproject.toml file. 
Builds and pushes a Docker image to a private docker hub repository.
Deploys the application on an EC2 instance with docker-compose.yaml file
and commits the version bump back to the repository.

CI/CD Demo:
https://user-images.githubusercontent.com/101016860/212427776-a30eca10-a17d-4cfd-90ed-6f1430df1e99.mp4

## Reference

CSS and the idea for this application came from [Angela Yu](https://github.com/angelabauer)
