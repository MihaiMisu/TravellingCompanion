# TravellingCompanion

This is the best app you'll ever experience. By using it, you can travel all over the world without having to bother<br>
about your schedule, cities or how much money you have left (none will remain, don't have hope).

# Getting started

A couple of settings must be done in order to get the application up and running.

##### 1. Create a config file for Django at path <em><b>TravellingCompanion/backend/config.json</b></em>.<br>
The template is the following one:<br>

```json
{
  "env": "<local/prod>",
  "allowedHosts": ["IP_1", "IP_2", "etc"],
  "secret": "<django_secret_key>",
  "DB_CONFIG": {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
      "NAME": "<DB_name>",
      "USER": "<DB_user>",
      "PASSWORD": "<DB_password>",
      "HOST": "<HOST>",
      "PORT": 1532
    }
  }
}
```
Note:<br>
- The <em>DB_name</em> has to be set accordingly to what name is given to the database at step 3
- The <em>DB_user</em> has to be set accordingly to what user is created in Postgres for the Django app. The Postgres\
 env file will contain the details to create an ADMIN user for a specific database (details at step 3), which can be\
 used for Django app. In this case replace <em>DB_user</em> by that username. If it's desired to use a different\
  user, then it must be created in Postgres first, then set inside this config file
- Same observation for <em>DB_password</em> as for the <em>DB_user</em>
<br><br>

##### 2. Create an env file for Django at path <em><b>TravellingCompanion/backend/env_config</b></em>.<br>
This file is used to provide details to create a superuser in order to have access into Django Admin app.<br>
The template file is the following one:<br>
```text
DJANGO_SUPERUSER_USERNAME=<username>
DJANGO_SUPERUSER_EMAIL=<email>
DJANGO_SUPERUSER_PASSWORD=<password>
```
Note:<br>
- Make sure that the email has the proper structure, otherwise there will be an error and the user won't be created
- This user can be used to login into the Admin application

##### 3. Create an env file for the database at path <em><b>TravellingCompanion/db_env</b></em>.<br>
The template file is the following one:<br>
```text
POSTGRES_USER=<db_admin>
POSTGRES_PASSWORD=<admin_psw>
POSTGRES_DB=<database_name>
```
Note:<br>
- These are the credentials to be used to connect to Postgres database as Admin
- As said at step 1 - notes, the ADMIN credentials (user, password) can be used inside the Django config file, as being\
 the user that Django uses to connect to database. Otherwise, it's needed to be created a new user and his credentials\
 to be set in the same way.
<br><br>

After setting up the config run the following command in the project's root folder <em><b>/TravellingCompanion</b></em>:

```docker
docker compose up --build
```
#### Important!!!
In order to run the unittests, the Django DB user must be able to create databases, so ensure it has rights.<br><br>
If a new DB user is wanted for Django app, it must be created in Postgres DB, set inside the file config from step 1\
and restart docker compose. Because when running for the first time the compose and both apps (Django and Postgres) will\
start, the Django app will raise an error because it's using a user for the database, that doesn't exist in the database.\
This is the reason why it should be created and after that it's needed to restart the compose.
```docker
docker-compose down (or CTRL-C if it's not run in detached/background mode)
docker compose up --build
```
<br>
Connection details:<br>
- Database:
<ul>
    <li>host: 127.0.0.1</li>
    <li>port: 5433</li>
    <li>Username: accordingly to <b>db_env</b> file (POSTGRES_USER)</li>
    <li>Password: accordingly to <b>db_enb</b> file (POSTGRES_PASSWORD)</li>
    <li>Database: accordingly to <b>db_enb</b> file (POSTGRES_DB)</li>
</ul>
- Django admin: 127.0.0.1:8001/admin
- REST API:
<ul>
    <li>trip/detail/</li>
    <li>trip/detail/<\uuid:trip_id\></li>
    <li>trip/manage/</li>
    <li>trip/manage/<\uuid:trip_id\></li>
    <li>trip/manage/<\uuid:trip_id\>/destination</li>
    <li>city/detail/</li>
    <li>city/detail/<\uuid:city_id\></li>
    <li>city/manage/</li>
    <li>city/manage/<\uuid:city_id\></li>
</ul>

