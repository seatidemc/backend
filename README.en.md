# backend

[简体中文](./README.md) | English

Here is the backend part of SEATiDE RESTful api. The backend simplifies the process of creating, starting and deleting Aliyun ECS instance for game playing, and also provides a platform for users to communicate with the database, which could be used to save Minecraft user data, user identity, levels & ranks, and so on in the not-too-distant future.

## Current implementations

### ECS Control with AccessKey & AccessSecret
  
Using a secret AccessKey & AccessSecret set to manage the ECSs. Any action will be recorded as history in the database. Using `type` in post requests to determine actual action. A token with administrator's permission is required to *POST* action api.

- *POST* `/api/ecs/v1/action`
  - `delete` — Forcefully delete current instance (*without confirmation*)
  - `new` — Create a preferred instance, then allocate a public ip for it, finally boot it.
  - `start` — Start the instance
  - `stop` — Stop the instance
- *GET* `/api/ecs/v1/describe/:name`
  - `available` — Check if the instance type is available to be created
  - `instance` — Get the detailed information of the preferred instance (type, bandwidth, disksize, zone)
  - `status` — Get the status of the current instance
  - `price` — Get the hourly price of the preferred instance
  - `last-invoke` — Get the results of the last invocation (only if `deploy` is set to `true`)

If `deploy` in `config.yml` is set to `true`, `src/run.sh` will be executed when the system is completely booted. Please make sure there is a `run.sh` in `src` directory before you enable `deploy`. **Note:** You can't use `~` in `run.sh`, which will lead to execution problems.

### User System

CRUD on users. Using `type` to determine actual action. A token with administrator's permission is required to *POST* action api.

- *POST* `/api/user/v1/action`
  - `create` — Create a new user with 3 required arguments: `username`, `password`, `email`
  - `get` — Get information of a user. *Incompatible with `password`*
  - `delete` — Delete a user
  - `alter` — Update a user's data using a ***k-v*** structure. *Incompatible with `password`*
  - `changepasswd` — Update a user's password
- *POST* `/api/user/v1/auth`
  - `auth` — Get login token with 7-day lifetime using username and password
  - `check` — Check if a token is valid, expired or invalid

**Note:** You must fill the `secret` in `config.yml` with random string (any value) to make it work.

## Deployment

**Requires Python 3.8+ and MySQL** This won't work under Python 3.8 (exclusive).

1. Clone the repository

```sh
git clone https://github.com/seatidemc/backend.git
```

2. (*Recommended but Optional*) Create a virtual environment

```sh
cd backend
python -m venv .
```

3. Install dependencies

```sh
pip install ./requirements.txt
cd src
unzip ./localdep.zip # Edited Aliyun Python SDK Core & Ecs
```

4. Initialize database. Just simply copy all the content in `.sql` and execute them in the MySQL command prompt. Please don't continue if there is any problem.
5. Rename `config.example.yml` to `config.yml` and change its content to suit your need. **Please make sure all the items marked as *required* are filled in properly**.

```sh
mv config.example.yml config.yml
vim config.yml
```

6. (*Optional*) Boot the api by running `app.py`. The type of server opening is depend on the `production` key in `config.yml`. If it's in production, the server will be open at port `8080`, otherwise `5000`.

```sh
python ./app.py
```
