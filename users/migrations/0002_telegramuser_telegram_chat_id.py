# Generated by Django 3.2.14 on 2022-07-06 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='telegram_chat_id',
            field=models.CharField(default=111, max_length=250),
            preserve_default=False,
        ),
    ]