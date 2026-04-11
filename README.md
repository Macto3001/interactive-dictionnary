# Interactive dictionnary

Interactive dictionnary is a python project made by me. It just consist of *2 app* one for the server and the other for the client.

you can search for any *word or sentence* you want and then give it a definition it will be stocked in the server.
There is also account witch you can create and then use to modify definition but it isn't fully implemented yet.

Unfortunatly i have no server at disposition to do that right now so there is no server but if you want to you can make a server with that yourself this project is just an test for now 

don't hesitate to upload thing it could help me a lot in this project

### it's still in developpment so a lot of feature just don't work

### also i made the virtual environement in linux so it don't work on windows for now but that will be add later

## how to run

first there are **two_version** you can run the *server* and the *client*
### run the client:
on linux terminal: use: 'source (YOUR_PROJECT_DIRECOTRY)/client/local_module/bin/activate' and then you can just launch the main.py with python: 'python (YOUR_PROJECT_DIRECOTRY)/client/main.py'

on windows for now you need to install the dependencies manually with pip see the list [here](#dependencies) and then it's the same in the cmd/powershell: 'python (YOUR_PROJECT_DIRECOTRY)/client/main.py'

### run the server:
on linux terminal: use 'source (YOUR_PROJECT_DIRECOTRY)/server/local_module/bin/activate' and then you need to go to the file directory so: 'cd (YOUR_PROJECT_DIRECOTRY)/server' and finally use uvicorn to create a server with the server-api.py: 'python -m uvicorn server-api:app'

for windows it's the same you just also need the dependencies [here](#dependencies) in your system so go to the server directory: 'cd (YOUR_PROJECT_DIRECOTRY)/server' and then use uvicorn to create a server with the server-api.py: 'python -m uvicorn server-api:app'

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