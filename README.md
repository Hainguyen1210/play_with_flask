# play_with_flask
a tiny project made while I following this course "REST APIs with Flask and Python Jose Salvatierra"

## How to install

#### install virtual envinronment

```shell
$ pip3 install virtualenv 
$ virtualenv -p python3 <your env name> # create your own venv
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

> add some samle data so we can test the APIs quicker.
> please open another terminal then run the following commands 

```shell
# to make sure the server can work well and tables are created
$ curl http://127.0.0.1:5000/items
$ python add_sample_data.py
```

#### import postman collection

Open your Postman client and hit `Command + O`, click `Choose Files` and head to this file `play_with_flask/chapter_6th/API_calls.postman_collection.json`.

After that, you can try to register new user and authenticate to get the JWT. The JWT token will be collected automatically so you do not need to do manual copy and paste, just call other APIs after an successful authentication. 

## APIs docs

> following are the endpoints along with their methods. Headers of all the `POST` request contains "Content-Type": "application/json". Some object modification requests, which is stated in each request description below, need the header "Authorization": "JWT {{JWT_TOKEN}}", if not, the request will receive status code `401`. 

___

#### user

> User authentication is required when accessing object-modification requests. This endpoints is to register new one and authenticate.

1. `POST` `/register`

   Request body:

   ```json
   {
   	"username": "<username>",
   	"password": "<password>"
   }
   ```

   Responses:

   ​	`201` 
   ```json
   {
	"messsage": "user name <username> craeted."
   }	
	```
	
	​	`400`
	
	```json
	{
	  "message": "user name <username> already exists."
	}
	```
	
2. `POST` `/auth`    

   Request body:  

   ```json
   {
     "username": "<username>",
     "password": "<password"
   }
   ```

   Responses:  

   ​	`200` - authentication success, use the token for other object-modification requests.

   ```json
   {
     "access_token": "<JWT token>"
   }
   ```

   ​	`401`

   ```json
   {
       "description": "Invalid credentials",
       "error": "Bad Request",
       "status_code": 401
   }
   ```

___

#### store

> store entity which holds items. 

1. `GET` `/stores`   

   Request body: `not required`

   Responses:

   ​	`200`
   > list all stores in the DB, along with links to their full info. 
   ```json
   {
   "stores": [
        {
            "name": "<store name>",
            "id": <store id>,
            "items": "<hostname>/store/<store name>"
        },
        ...
        ]
   }	
   ```
   
2. `GET` `/stores/<name>`

   Request body: `not required`

   Responses:

   ​	`200` 
   
   > show store's info and all its items
	
   ```json
	{
	    "name": "<store name>",
	    "id": <store id>,
	    "items": [
	        {
	            "name": "<item name>",
	            "price": <item price>,
	            "store_id": <store id>
	        },
	      	...
	    ]
	}
	```
	
   ​	`400` 
   
   ```json
	{
       "message": "store not found"
	}
	```
	
3. `POST` `/stores/<name>`  

   > Header "Authorization": "JWT {{JWT_TOKEN}}" is required

   Request body: `not required` 

   Responses:

   ​	`201`  - a new store has been successfully created 
   ```json
   {
    "name": "<store name>",
    "id": <store id>,
    "items": []
}
	```
	
	​	`400`
	
	```json
	{
	  "message": "A store with name <store name> already exists."
	}
	```
	
4. `DELETE` `/stores/<name>`  

   > Header "Authorization": "JWT {{JWT_TOKEN}}" is required

   Request body: `not required`
   
   Responses:

   ​	`200` 
   ```json
   {
	"messsage": "store has been deleted."
   }	
	```
	
	​	`400`
	
	```json
	{
	  "message": "cannot delete store that contains items."
	}
	```
	
	​	`404`
	
	```json
	{
	  "message": "store not found."
	}
	```
	
5. `PUT` `/stores/<name>`  

   > Header "Authorization": "JWT {{JWT_TOKEN}}" is required

   Request body:

   ```json
   {
   	"new_name": "<new store name>"
   }
   ```
   

Responses:

​	`200` - if the store exists, update its name with the new name specified in <new_name>
   ```json
   {
   "messsage": "store has been updated."
	}	
   ```

		`201` - if the store does not exist, create a new one with `<name>`
	
	```json
	{
	  "message": "store has been added."
	}
	```

___

#### item

> each created item needs to be associated with one existing store

1. `GET` `/items`  

   > list all stores in the DB, along with links to their full info.   
   
   Request body: `not required`

   Responses:
   
   ​	`200`
   ```json
   {
       "items": [
           {
               "name": "car",
               "price": 200,
               "store_id": 2
           },
           ...
       ]
   }
   ```

2. `GET` `/items/<name>`  
   Responses:
   
   ​	`200`
   ```json
   {
       "name": "<item name>",
       "price": <item price>,
       "store_id": <store id>
   }
   ```
   
   ​	`404`
   ```json
   {
       "message": "item not found"
   }
   ```
   
3. `POST` `/items/<name>`

   > Header "Authorization": "JWT {{JWT_TOKEN}}" is required

   Request body:   

   ```json
   {
     "price": <price>,
     "store_id": <store id>
   }
   ```

   
   Responses:  

   ​	`201`  - a new store has been successfully created 
   ```json
   {
    "name": "<store name>",
    "id": <store id>,
    "items": []
   }
   ```

   ​	`400`
   ```json
   {
     "message": "A store with name <store name> already exists."
   }
   ```
   or 
   ```json
   {
     "message": "Item must be defined with its price and store_id."
   }
   ```
   or 
   ```json
   {
     "message": "store_id is not found."
   }
   ```

4. `DELETE` `/items/<name>`  

   > Header "Authorization": "JWT {{JWT_TOKEN}}" is required

   Request body: `not required`
   
   Responses:

   ​	`200` 
   ```json
   {
	"messsage": "item has been deleted."
   }	
	```
	
	​	`404`
	
	```json
	{
	  "message": "item not found."
	}
	```



5. `PUT` `/items/<name>`

   > Header "Authorization": "JWT {{JWT_TOKEN}}" is required

   Request body:

   ```json
   {
   	"price": <price>,
     "store_id": <store id>
   }
   ```
   Responses:
   
   ​	`200` - if the store exists, update it with new `price` and `store_id`
   ```json
   {
	"messsage": "item has been updated."
   }	
	```
	
   ​	`201` 
   ```json
   {
	"messsage": "item has been added."
   }	
	```

___

