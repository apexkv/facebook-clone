# **Users Microservice**

## Table of Contents

## Overview

The Users microservice handles user authentication, registration, and profile management. It provides APIs for managing user data such as profile pictures, names, and account details. The service propagates user updates to other microservices (e.g., Posts and Friends) using RabbitMQ. It acts as the central source of user information across the system.

## Features

-   User authentication and registration
-   Profile management
-   JWT token generation and validation
-   RESTful API for user operations
-   Secure communication with JWT authentication

## Used Technologies

-   Django
-   Django Restframework
-   Postgresql
-   RabbitMQ
-   Redis

## Environment Variables

```plaintext
SECRET_KEY=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_ROOT_PASSWORD=
POSTGRES_PORT=

RABBITMQ_DEFAULT_USER=
RABBITMQ_DEFAULT_PASS=
RABBITMQ_HOST=

CURRENT_QUEUE=users
QUEUE_LIST=friends,posts,chat
```

## API Documentation

# Authentication

-   HTTP Authentication, scheme: basic

<h1 id="fb-clone-users-api-users">users</h1>

## users_login_create

<a id="opIdusers_login_create"></a>

> Code samples

```http
POST /api/users/login/ HTTP/1.1

Content-Type: application/json
Accept: application/json

```

`POST /users/login/`

Login User

> Body parameter

```json
{
    "email": "user@example.com",
    "password": "stringst"
}
```

<h3 id="users_login_create-parameters">Parameters</h3>

| Name | In   | Type                          | Required | Description |
| ---- | ---- | ----------------------------- | -------- | ----------- |
| body | body | [UserLogin](#schemauserlogin) | true     | none        |

> Example responses

> 200 Response

```json
{
    "id": "string",
    "email": "user@example.com",
    "full_name": "string",
    "password": "string"
}
```

<h3 id="users_login_create-responses">Responses</h3>

| Status | Meaning                                                          | Description | Schema                        |
| ------ | ---------------------------------------------------------------- | ----------- | ----------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)          | none        | [User](#schemauser)           |
| 400    | [Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1) | none        | [UserLogin](#schemauserlogin) |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
Basic
</aside>

## users_me_read

<a id="opIdusers_me_read"></a>

> Code samples

```http
GET /api/users/me/ HTTP/1.1

Accept: application/json

```

`GET /users/me/`

Retrieve User

> Example responses

> 200 Response

```json
{
    "id": "string",
    "email": "user@example.com",
    "full_name": "string",
    "password": "string"
}
```

<h3 id="users_me_read-responses">Responses</h3>

| Status | Meaning                                                         | Description  | Schema              |
| ------ | --------------------------------------------------------------- | ------------ | ------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)         | none         | [User](#schemauser) |
| 401    | [Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1) | Unauthorized | None                |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
Basic
</aside>

## users_refresh_create

<a id="opIdusers_refresh_create"></a>

> Code samples

```http
POST /api/users/refresh/ HTTP/1.1

Content-Type: application/json
Accept: application/json

```

`POST /users/refresh/`

Takes a refresh type JSON web token and returns an access type JSON web
token if the refresh token is valid.

> Body parameter

```json
{
    "refresh": "string"
}
```

<h3 id="users_refresh_create-parameters">Parameters</h3>

| Name | In   | Type                                | Required | Description |
| ---- | ---- | ----------------------------------- | -------- | ----------- |
| body | body | [TokenRefresh](#schematokenrefresh) | true     | none        |

> Example responses

> 201 Response

```json
{
    "refresh": "string",
    "access": "string"
}
```

<h3 id="users_refresh_create-responses">Responses</h3>

| Status | Meaning                                                      | Description | Schema                              |
| ------ | ------------------------------------------------------------ | ----------- | ----------------------------------- |
| 201    | [Created](https://tools.ietf.org/html/rfc7231#section-6.3.2) | none        | [TokenRefresh](#schematokenrefresh) |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
Basic
</aside>

## users_register_create

<a id="opIdusers_register_create"></a>

> Code samples

```http
POST /api/users/register/ HTTP/1.1

Content-Type: application/json
Accept: application/json

```

`POST /users/register/`

Create User

> Body parameter

```json
{
    "email": "user@example.com",
    "full_name": "string",
    "password": "string"
}
```

<h3 id="users_register_create-parameters">Parameters</h3>

| Name | In   | Type                | Required | Description |
| ---- | ---- | ------------------- | -------- | ----------- |
| body | body | [User](#schemauser) | true     | none        |

> Example responses

> 200 Response

```json
{
    "refresh": "string",
    "access": "string"
}
```

<h3 id="users_register_create-responses">Responses</h3>

| Status | Meaning                                                          | Description | Schema                |
| ------ | ---------------------------------------------------------------- | ----------- | --------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)          | none        | [Token](#schematoken) |
| 400    | [Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1) | none        | [User](#schemauser)   |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
Basic
</aside>

## users_update_update

<a id="opIdusers_update_update"></a>

> Code samples

```http
PUT /api/users/update/ HTTP/1.1

Content-Type: application/json
Accept: application/json

```

`PUT /users/update/`

Create User

> Body parameter

```json
{
    "email": "user@example.com",
    "full_name": "string",
    "password": "string"
}
```

<h3 id="users_update_update-parameters">Parameters</h3>

| Name | In   | Type                | Required | Description |
| ---- | ---- | ------------------- | -------- | ----------- |
| body | body | [User](#schemauser) | true     | none        |

> Example responses

> 200 Response

```json
{
    "id": "string",
    "email": "user@example.com",
    "full_name": "string",
    "password": "string"
}
```

<h3 id="users_update_update-responses">Responses</h3>

| Status | Meaning                                                 | Description | Schema              |
| ------ | ------------------------------------------------------- | ----------- | ------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | none        | [User](#schemauser) |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
Basic
</aside>

## users_read

<a id="opIdusers_read"></a>

> Code samples

```http
GET /api/users/{id}/ HTTP/1.1

Accept: application/json

```

`GET /users/{id}/`

<h3 id="users_read-parameters">Parameters</h3>

| Name | In   | Type   | Required | Description |
| ---- | ---- | ------ | -------- | ----------- |
| id   | path | string | true     | none        |

> Example responses

> 200 Response

```json
{
    "id": "string",
    "email": "user@example.com",
    "full_name": "string",
    "password": "string"
}
```

<h3 id="users_read-responses">Responses</h3>

| Status | Meaning                                                 | Description | Schema              |
| ------ | ------------------------------------------------------- | ----------- | ------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | none        | [User](#schemauser) |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
Basic
</aside>

## users_delete

<a id="opIdusers_delete"></a>

> Code samples

```http
DELETE /api/users/{id}/ HTTP/1.1

```

`DELETE /users/{id}/`

<h3 id="users_delete-parameters">Parameters</h3>

| Name | In   | Type   | Required | Description |
| ---- | ---- | ------ | -------- | ----------- |
| id   | path | string | true     | none        |

<h3 id="users_delete-responses">Responses</h3>

| Status | Meaning                                                         | Description | Schema |
| ------ | --------------------------------------------------------------- | ----------- | ------ |
| 204    | [No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5) | none        | None   |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
Basic
</aside>

# Schemas

<h2 id="tocS_UserLogin">UserLogin</h2>
<!-- backwards compatibility -->
<a id="schemauserlogin"></a>
<a id="schema_UserLogin"></a>
<a id="tocSuserlogin"></a>
<a id="tocsuserlogin"></a>

```json
{
    "email": "user@example.com",
    "password": "stringst"
}
```

### Properties

| Name     | Type          | Required | Restrictions | Description |
| -------- | ------------- | -------- | ------------ | ----------- |
| email    | string(email) | true     | none         | none        |
| password | string        | true     | none         | none        |

<h2 id="tocS_User">User</h2>
<!-- backwards compatibility -->
<a id="schemauser"></a>
<a id="schema_User"></a>
<a id="tocSuser"></a>
<a id="tocsuser"></a>

```json
{
    "id": "string",
    "email": "user@example.com",
    "full_name": "string",
    "password": "string"
}
```

### Properties

| Name      | Type          | Required | Restrictions | Description |
| --------- | ------------- | -------- | ------------ | ----------- |
| id        | string        | false    | read-only    | none        |
| email     | string(email) | true     | none         | none        |
| full_name | string        | true     | none         | none        |
| password  | string        | true     | none         | none        |

<h2 id="tocS_TokenRefresh">TokenRefresh</h2>
<!-- backwards compatibility -->
<a id="schematokenrefresh"></a>
<a id="schema_TokenRefresh"></a>
<a id="tocStokenrefresh"></a>
<a id="tocstokenrefresh"></a>

```json
{
    "refresh": "string",
    "access": "string"
}
```

### Properties

| Name    | Type   | Required | Restrictions | Description |
| ------- | ------ | -------- | ------------ | ----------- |
| refresh | string | true     | none         | none        |
| access  | string | false    | read-only    | none        |

<h2 id="tocS_Token">Token</h2>
<!-- backwards compatibility -->
<a id="schematoken"></a>
<a id="schema_Token"></a>
<a id="tocStoken"></a>
<a id="tocstoken"></a>

```json
{
    "refresh": "string",
    "access": "string"
}
```

### Properties

| Name    | Type   | Required | Restrictions | Description |
| ------- | ------ | -------- | ------------ | ----------- |
| refresh | string | true     | none         | none        |
| access  | string | true     | none         | none        |

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
