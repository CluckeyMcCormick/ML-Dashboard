# ML-Dashboard

This is a Django webapp designed for a small charity organization, [Million Little](https://www.millionlittle.com/). It was developed in **Python 3** and was intended to be hosted on **Heroku**.

It serves several functions:

* Manages contact information 

* Provides basic project management functionality - assigning contacts, setting deadlines, tasking, etc.

* Allows for the information to be downloaded in an excel file

It's a very basic project but it provides just the right amount of utility for the charity in question.

## Configuring the Environment

Django stores some important, secret values in plain text (for reasons that are beyond me). I've configured the app to look for two environment variables:

* `SECRET_KEY` - The secret key used to salt passwords. ***I cannot heavily recommend enough that you provide a non-default value for the secret key***. Django provides a random value in new Django projects, and you can also look up how to generate a key.

* `HOST_NAME` - The address the website will be hosted at. By default, this is `127.0.0.1`, which works for running it locally.

Default values are provided, for more information, look in dashboard/settings.py. 

These environment variables can easily be set in a **Heroku** app by [adding some extra config variables](https://devcenter.heroku.com/articles/config-vars).

## Running the Webapp (Locally)

> Note: this project requires **Python 3** and it's module installer, **pip**. As such, the following commands will be using Python 3 specific commands; i.e. **pip3** rather than **pip**.

The process for running the webapp locally is much the same as any Django app. Start by installing the required python packages:

```bash
cd where/ever/the/local/repo/is
sudo pip3 install -r requirements.txt
```

Next, use the *migrate* command to create the appropriate database:

```bash
python3 manage.py migrate
```

Finally, use the *runserver* command to run the server:

```bash
python3 manage.py runserver
```
 
Once the webapp is running, there is additional setup required before the webapp is usable - see *Setting up a User* below.

## Setting up a User

Whenever a user logs in, the web app retrieves the information about their associated tasks, projects, events, etc. This requires a link between a *Contact* object and a *User* object.

The webapp provides a native (i.e. not through the admin interface) way to create users, BUT you can only access it with the appropriate permissions. What we get is a chicken and the egg situation. The solution is this:

0. Create superuser

0. Create contact for superuser

0. Verify

### 1. Create superuser

First, we'll create a superuser so that we can access the admin interface (it's a good idea to have a superuser account, anyway).

```bash
cd where/ever/the/local/repo/is
python3 manage.py createsuperuser
```

This will create a superuser with the username and password you provide.

### 2. Create contact for superuser

Ensure that the server is running, then visit the website using a web browser. You will be directed to the login screen.

Log in to the super user account you just created - you will be redirected to an error screen. The URL should be something like `[hostname]/contact_app/`. You can access the admin screen by changing the URL to `[hostname]/admin/`. 

Once at the admin screen, press the **Add** button next to the **Contacts** object. 

Enter some contact information (preferably your own). At the bottom will be a field called **User Link**. Use it to select the superuser account you just created. Then, press the **SAVE** button.

### 3. Verify

To verify that the process worked, press **View Site**, located in the upper-right hand corner of the admin page. You should see the default dashboard.

