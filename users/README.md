# Users

This microservice is for handle user authentications and authorizations. This server runs on `port 8010`. These are urls and responses from this service.

### User Login

> /api/user/login/

POST

```
{
    "email": string,
    "password": string,
}
```

RESPONSE

```
HTTP 400 Bad Request
{
    "email": string[],
    "password": string[]
}

HTTP 200 OK
{
    "tokens": {
        "refresh": string,
        "access": string
    },
    "data": {
        "id": string,
        "full_name": string,
        "email": string,
        "profile_pic": string, # hyperlink for image
    }
}
```

### Register User

> /api/user/register/

POST

```
{
    "email": string,
    "full_name": string,
    "profile_pic": null, # image data
    "password": string
}
```

RESPONSE

```
HTTP 400 Bad Request
{
    "email": string[],
    "full_name": string[],
    "profile_pic": string[],
    "password": string[],
}

HTTP 201 Created
{
    "id": string,
    "full_name": string,
    "email": string,
    "profile_pic": string, # hyperlink for image
}
```

### Validate User and Get User using Access Token

> /api/user/me/

GET

```
Header:{
    Authorization: JWT <access_token>
}
```

RESPONSE

```
HTTP 401 Unauthorized
{
    "detail": string,
    "code": "token_not_valid",
}
```

### Update User Data

> /api/user/update/

PUT

```
{
    "email": string,
    "full_name": string,
    "profile_pic": null, # image data, set null for delete image
    "password": string
}
```

RESPONSE

```
HTTP 200 OK
{
    "id": string,
    "full_name": string,
    "email": string,
    "profile_pic": string, # hyperlink for image
}

HTTP 400 Bad Request
{
    "email": string[],
    "full_name": string[],
    "profile_pic": string[],
    "password": string[],
}
```

### Refresh User Token

> /api/user/refresh/

POST

```
{
    "refresh": string
}
```

RESPONSE

```
HTTP 405 Method Not Allowed
{
    "detail": string,
}

HTTP 400 Bad Request
{
    "refresh": string[]
}

HTTP 401 Unauthorized
{
    "detail": string,
    "code": "token_not_valid",
}
```

### Get User Profile Picture

> /api/user/media/<image_name:str>

```
This will return image
```
