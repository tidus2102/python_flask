uPaty API References
====================

Accounts
--------

**Create new account**

- Endpoint: /users
- Method: POST
- Params: 
    - **full_name** (string)
    - **email** (string)
    - **fb_id** (string)
    - **fb_token** (string)
    - **avatar** (file)
    - **device_id** (string)
- Response:

```
{  
  "id": 111,
  "full_name": "string",
    "email": "string",
    "fb_id": "string",
    "fb_token": "string",
    "avatars": {
       "origin": "origin_url",
       "small": "small_url",
       "thumb": "thumb_url",
    },
    "access_token": "string",
    "device_id": "string",      
}
```

**Get account details**:

- Endpoint: /users/<user_id>
- Method: GET
- Params: NO
- Response:

```
{
    "id": 111,
    "full_name": "string",
    "email": "string",
    "fb_id": "string",
    "avatars": {
       "origin": "origin_url",
       "small": "small_url",
       "thumb": "thumb_url",
    },
}
```

**Update account information**

- Endpoint: /users/<user_id>
- Method: PUT
- Params: 
    - **full_name** (string)
    - **email** (string)
    - **avatar** (file)
- Response:

```
{
     "id": 111,
     "full_name": "string",
     "email": "string",
     "fb_id": "string",
     "avatars": {
       "origin": "origin_url",
       "small": "small_url",
       "thumb": "thumb_url",
    },
}
```