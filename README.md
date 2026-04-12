# Interactive dictionnary

Interactive dictionnary is a python project made by me. It just consist of *2 app* one for the server and the other for the client.

you can search for any *word or sentence* you want and then give it a definition it will be stocked in the server.
There is also account witch you can create and then use to modify definition but it isn't fully implemented yet.

Unfortunatly i have no server at disposition to do that right now so there is no server but if you want to you can make a server with that yourself this project is just an test for now 

don't hesitate to upload thing it could help me a lot in this project

### it's still in developpment so a lot of feature just don't work

## how to run

first there are **two_version** you can run the *server* and the *client*
### run the client:
first go to the project folder then create a python venv of the name you want, enter in it, and add the dependencies in requirements.txt and then you can just launch the main.py with python:
- ```cd <project_dir>```
- ```python -m venv <venv_name>```
- on win: ```./<venv_name>/Scripts/activate```, on linux: ```source <venv_name>/bin/activate```
- ```python -m pip -r client/requirements.txt```
- ```python client/main.py```

### run the server:
first go to the project folder then create a python venv of the name you want, enter in it, and add the dependencies in requirements.txt and then you can just launch the server-api.py with python:
- ```cd <project_dir>```
- ```python -m venv <venv_name>```
- on win: ```./<venv_name>/Scripts/activate```, on linux: ```source <venv_name>/bin/activate```
- ```python -m pip -r server/requirements.txt```
- ```python server/server-api.py```

## dependencies
there are 3 dependencies on this project:
- for the client there is:
    - requests
- for the server there are:
    - fastapi
    - request

you also need python to run this it isn't compiled 

## other thing
there is a [changlog](changelog.txt) where you can see every thing i did

i'm alone on this project but if you want to help me you can totally