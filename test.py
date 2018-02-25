import logging
import logging.config
from unittest import TestCase

from pylog_telegram.telegram_handler import PylogTelegramHandler, MarkdownFormatter


class TestTelegramHandler(TestCase):
    def setUp(self):

        self.chat_id = ''
        self.token = ''

    def test_simple(self):
        handler = PylogTelegramHandler(self.chat_id, self.token)
        logger = logging.getLogger('root')
        logger.propagate=False
        logger.setLevel(logging.DEBUG)
        formatter = MarkdownFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        try:
            1 / 0
        except Exception as e:
            logger.exception(e)

    def test_config(self):

        logging.config.fileConfig('config.txt')
        logger = logging.getLogger('root')
        try:
            1 / 0
        except Exception as e:
            logger.exception(e)

    def test_dictconfig(self):

        logconfig = {
            'version': 1,
            'handlers': {
                'telegram': {
                    'formatter': 'html',
                    'class': 'pylog_telegram.telegram_handler.PylogTelegramHandler',
                    'chat_id': '-1001321844132',
                    'token': '481764146:AAELlGNC8TggdBtQR9e64nqc47lC-LOXMCQ',
                }
            },
            'formatters': {
                'html': {
                    'class': 'pylog_telegram.telegram_handler.HtmlFormatter'
                },
            },
            'loggers': {
                'root': {
                    'level': 'DEBUG',
                    'handlers': ['telegram'],
                    'propagate': False

                }
            }
        }
        logging.config.dictConfig(logconfig)
        logger = logging.getLogger('root')
        try:
            1 / 0
        except Exception as e:
            logger.exception(e)
