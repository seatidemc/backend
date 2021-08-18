# backend

Here is the backend part of SEATiDE RESTful api. The backend simplifies the process of creating, starting and deleting Aliyun ECS instance for game playing, and also provides a platform for users to communicate with the database, which could be used to save Minecraft user data, user identity, levels & ranks, and so on in the not-too-distant future.

## Current implementations

ECS Control with AccessKey & AccessSecret
  
Using a secret AccessKey & AccessSecret set to manage the ECSs. Any action will be recorded as history in the database. **Note:** Currently there is no authentication system.

- `/api/ecs/v1/action/:action`
    - `delete` — Forcefully delete current instance
    - `new` — Create a instance using the preferences set in `config.yml`
    - `init` — Allocate public ip and start the newly created instance
    - `start` — Start the instance
    - `stop` — Stop the instance
- `/api/ecs/v1/describe/:name`
    - `available` — Check if the instance type is available to be created
    - `instance` — Get the instance detailed information (type, bandwidth, disksize, zone)
    - `status` — Get the status of the current instance
    - `price` — Get the hourly price of the preferred instance

## Deployment

**Requires Python 3.8+** This won't work under 3.8 (exclusive).

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
```

4. Initialize database. Just simply copy all the content in `.sql` and execute them in the MySQL command prompt. Please don't continue if there is any problem.
5. Rename `config.example.yml` to `config.yml` and change its content to suit your need. **Please make sure all the items marked as *required* are filled in properly**

```sh
mv config.example.yml config.yml
vim config.yml
```

6. (*Optional*) If you want to test the api in your local environment, just start the development server by running `src/app.py`.

```sh
cd src
python ./app.py
```