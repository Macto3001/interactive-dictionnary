there are 4 dependencies to this project:
- Client side:
	- requests
- Server side:
	- fastapi
	- pickle
	- uvicorn

you also obviously need python to run the program

to run it on client just do "python "YOURPROJECTFOLDER"/client/main.py"

to run it on server do "cd "YOURPROJECTFOLDER"/server/" and then "python -m uvicorn server-api:app"