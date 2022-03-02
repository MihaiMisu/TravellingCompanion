# TravellingCompanion

This is the best app you'll ever experience. By using it, you can travel all over the world without<br>
having to bother about your schedule, cities or how much money you have left <br>
(none will remain, don't have hope).

# Getting started

To bring the code alive, it's needed a config file to be saved at /backend/config.json.<br>
The template is the following one:<br>

```json
{
  "env": "<local/prod>",
  "allowedHosts": [<list of IPs>],
  "secret": <django_secret_key>,
  "DB_CONFIG": {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
      "NAME": "<DB_name>",
      "USER": "<DB_user>",
      "PASSWORD": "<DB_password>",
      "HOST": "<HOST>",
      "PORT": <PORT>
    }
  }
}
```

After setting up the config run the following command in the project's root folder:

```docker compose up --build```

