# APIs docs

Following are the endpoints along with their methods. Headers of all the `POST` request contains "Content-Type": "application/json".  
Some requests, which are marked with `authentication required`, need the header `"Authorization": "JWT {{JWT_TOKEN}}"`.
Otherwise, the request will receive status code `401`.

---
## **user**
User authentication is required when accessing object-modification requests. This endpoints is to register new one and authenticate.

1. `POST` `/register`

    Request body:

    ```json
    {
        "username": "<username>",
        "password": "<password>"
    }
    ```

    Responses:

    `201`
    ```json
    {
        "message": {
           "msg": "User name <username> created"
        }
    }
    ```

    `400`
    ```json
    {
        "message": {
           "msg": "User name <username> already exists"
        }
    }
    ```
    or
    ```json
    {
        "message": {
            "username": "Must be 4-20 non-whitespace characters long"
        }
    }
    ```
    or
    ```json
    {
        "message": {
            "password": "Must be 8-20 characters long"
        }
    }
    ```


2. `POST` `/auth`

    Request body:

    ```json
    {
        "username": "<username>",
        "password": "<password>"
    }
    ```

    Responses:

    `200` - authentication success, use the token for other object-modification requests.
    ```json
    {
        "access_token": "<JWT token>"
    }
    ```

    `401`
    ```json
    {
        "description": "Invalid credentials",
        "error": "Bad Request",
        "status_code": 401
    }
    ```  
    
---
## **store**

1. `GET` `/stores`  
    List all stores in the DB, along with links to their full info.

    Request body: None

    Responses:

    `200`
    ```
    [
        {
            "name": "<store name>",
            "id": <store id>
        },
        ...
    ]
    ```

2. `GET` `/stores/<int:store_id>`  
    Show store's info and all its items

    Request body: None

    Responses:

    `200`
    ```
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

    `400`
    ```json
    {
        "message": {
           "msg": "Store id:<store_id> not found"
        }
    }
    ```

3. `POST` `/stores`  
    `authentication required`

    Request body:
    {
        "name": "<store_name>"
    }

    Responses:

    `201`
    ```
    {
        "name": "<store name>",
        "id": <store id>
    }
    ```

    `400`
    ```json
    {
        "message": {
            "name": "Must be less than 80 characters"
        }
    }
    ```

4. `DELETE` `/stores/<int:store_id>`  
    `authentication required`

    Request body: None

    Responses:

    `200`
    ```json
    {
        "message": {
           "msg": "Store <store_id> deleted"
        }
    }
    ```

    `404`
    ```json
    {
        "message": {
           "msg": "Store id:<store_id> not found"
        }
    }
    ```

    `400`
    ```json
    {
        "message": {
           "msg": "Cannot delete store that contains items"
        }
    }
    ```

5. `PUT` `/stores/<name>`  
    `authentication required`

    Request body:
    ```json
    {   
        "new_name": "<new store name>"
    }
    ```

    Responses:

    `200` - if the store exists, update its name with the new name specified in <new_name>
    ```json
    {
        "message": {
           "msg": "Store updated"
        }
    }
    ```

    `404`
    ```json
    {
        "message": {
           "msg": "Store id:<store_id> not found"
        }
    }
    ```
    `400`
    ```json
    {
        "message": {
           "new_name": "Must be less than 80 characters"
        }
    }
    ```

---
## **item**

1. `GET` `/items`

    List all items in the DB

    Request body: None
    
    Responses:
    `200`
    ```
    [
        {
            "id": 1
            "name": "car",
            "price": 200,
            "store_id": 2
        },
        ...
    ]
    ```

2. `GET` `/stores/<store_id>/items`

    List all items that belong to the store with id <store_id>

    Request body: None
    
    Responses:
    `200`
    ```
    [
        {
            "id": 2, 
            "name": "car",
            "price": 200,
            "store_id": 2
        },
        ...
    ]
    ```

3. `GET` `/stores/<store_id>/items/<item_id>`

    Request body: None
    
    Responses:
    
    `200`
    ```json
    {
        "id": 2, 
        "name": "car",
        "price": 200,
        "store_id": 2
    }
    ```

    `404`
    ```json
    {
        "message": {
            "msg": "Store id:<store_id> not found" 
        }
    }
    ```
    or
    ```json
    {
        "message": {
            "msg": "Item id:<item_id> not found" 
        }
    }
    ```

4. `DELETE` `/stores/<store_id>/items/<item_id>`  
    `authentication required`

    Request body: None
    
    Responses:
    
    `200`
    ```json
    {
        "message": {
            "msg": "Item <item_id> deleted"
        }
    }
    ```

    `404`
    ```json
    {
        "message": {
            "msg": "Item id:<item_id> not found" 
        }
    }
    ```

5. `POST` `/stores/<store_id>/items`  
    `authentication required`

    Request body:
    
    ```
    {
        "name": "<item name>"
        "price": <price>,
    }
    ```
    
    Responses:
    
    `201`
    ```
    {
        "id": <item_id>,
        "name": "<item_name>",
        "price": <price>,
        "store_id": <store_id>
    }
    ```
    
    `404`
    ```json
    {
        "message": {
            "msg": "Store id:<store_id> not found" 
        }
    }
    ```

    `400`
    ```json
    {
        "message": {
            "name": "Must be less than 80 characters" 
        }
    }
    ```
    or
    ```json
    {
        "message": {
            "price": "Must be positive" 
        }
    }
    ```

6. `PUT` `/stores/<store_id>/items/<item_id>`  
    `authentication required`

    Request body:
    
    ```
    {
        "new_name": "<item_name>",
        "new_price": <price>,
    }
    ```
    
    Responses:
    
    `200` 
    ```json
    {
        "message": {
            "msg": "Item updated"
        }
    }
    ```
    
    `404`
    ```json
    {
        "message": {
            "msg": "Store id:<store_id> not found" 
        }
    }
    ```
    or
    ```json
    {
        "message": {
            "msg": "Item id:<item_id> not found" 
        }
    }
    ```

    `400`
    ```json
    {
        "message": {
            "msg": "Nothing to update" 
        }
    }
    ```
    or
    ```json
    {
        "message": {
            "new_name": "Must be less than 80 characters" 
        }
    }
    ```
    or
    ```json
    {
        "message": {
            "new_price": "Must be positive" 
        }
    }
    ```
