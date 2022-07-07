# Django + Telegram bot
The goal of this project is to create a telegram bot with a Django admin panel.
Using [the telegram bot](https://t.me/test_django_telegram_bot "the telegram bot") you can register on the service. Also, there are commands to restore access to the account, such as `/remind_login` and `/change_password`.

When creating an account, it checks if the user already exists. It is assumed that one telegram user has one account.

The password will be validated using the existing Django validator. If there is a mismatch, the user will be warned that their password is not strong enough.

The password will be requested twice so that the user is sure of writing it. If the password does not match, the user will be prompted to start setting the password again.

The site https://django-and-telegram-bot.herokuapp.com/ contains user data. To see them, the user must log in to the site.

Using the admin panel, you can view and edit information about users.
Login information for the admin panel:
- login: admin
- password: admin

# Technology

- Python 3.10

- Django 3.2.13

- Aiogram 2.21

- Postgresql

- Heroku


# Installation 

## Local

1. Clone the repository

2. Create a virtual environment in the root folder `python -m venv venv`

3. Activate the virtual environment `venv\Scripts\activate.bat`

4. Install the dependencies `pip install -r requirements.txt`

5. Copy and fill in with your data `cp .env.example .env`

6. Run database migrations `python manage.py migrate`

7. To start the server, enter `python manage.py runserver`

8. To start the bot, enter `python manage.py runbot`


## Heroku
1. Set up environment variables Heroku in Setting/Config_Vars

2. Log in to your Heroku

3. Use Git to clone app's source code to your local machine

4. Deploy app to Heroku using Git - `git push heroku main`




