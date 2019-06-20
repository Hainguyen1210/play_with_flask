# play_with_flask
a tiny project made while I following this course "REST APIs with Flask and Python Jose Salvatierra"

## How to install

#### install virtual envinronment

```shell
$ pip3 install virtualenv
$ virtualenv -p python3 <your env name# create your own venv
$ source <your env name>/bin/activate # activate it
```

#### install python packages

```shell
$ pip3 install -r requirement.txt
```

#### start the server

```shell
# since this is the most robust one, please ignore other two chapters.
$ cd chapter_6th/
$ python app.py
# you should see something like this in the output
# Running on http://127.0.0.1:5000/
```

#### import sample data to DB [optional]    

Add some sample data so we can test the APIs quicker. Please open another terminal then run the following commands

```shell
# to make sure the server can work well and tables are created
$ curl http://127.0.0.1:5000/items
$ python add_sample_data.py
```

#### import postman collection  

Open your Postman client and hit `Command + O`, click `Choose Files` and head to this file `play_with_flask/chapter_6th/API_calls.postman_collection.json`.

After that, you can try to register new user and authenticate to get the JWT. The JWT token will be collected automatically so you do not need to do manual copy and paste, just call other APIs after an successful authentication.

## APIs docs
[moved here](APIs%20docs.md)