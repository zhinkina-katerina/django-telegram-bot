from django.core.management.base import BaseCommand

from telegram_bot.main import executor

class Command(BaseCommand):

    def handle(self, *args, **options):
        executor()