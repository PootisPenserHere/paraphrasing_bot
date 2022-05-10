import requests

from paraphrasing_bot.src.services.Config import Config as ConfigService
from paraphrasing_bot.src.services.String import String as StringService


class Bootstrap:
    def __init__(self):
        self.config_service = ConfigService()
        self.string_service = StringService()

        self._set_telegram_webhook()

    def _set_telegram_webhook(self):
        # TODO move the telegram fragment of the uri to a constant used in the routes
        webhook_url = self.string_service.url_builder(
            self.config_service.BACKEND_ADDRESS,
            '/webhook/telegram'
        )

        webhook_register_url = self.string_service.url_builder(
            'https://api.telegram.org/bot/',
            self.config_service.TELEGRAM_TOKEN,
            '/setWebHook?url=',
            webhook_url
        )

        r = requests.get(webhook_register_url)
        print(r.json())
