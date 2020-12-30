from telegram.ext import Updater
from django.conf import settings

bot = Updater(token=settings.BOT_TOKEN, use_context=True)
