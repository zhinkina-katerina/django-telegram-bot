from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers  import make_password

class TelegramUser(AbstractUser):
    telegram_fullname = models.CharField(max_length=250)
    telegram_username = models.CharField(max_length=250)
    telegram_user_id = models.CharField(max_length=250)
    telegram_chat_id = models.CharField(max_length=250)


class TelegramUserProvider:
    @staticmethod
    async def create_or_update_user(telegram_fullname, telegram_username, telegram_user_id, login, password):
        try:
            was_created_or_update = TelegramUser.objects.update_or_create(
                telegram_user_id=telegram_user_id,
                defaults={
                    'telegram_fullname':telegram_fullname,
                    'telegram_username':telegram_username,
                    'username': login,
                    'password':make_password(password)
                },
            )
            return was_created_or_update[1], None
        except Exception as e:
            return False, "Error: \n" + str(e)
