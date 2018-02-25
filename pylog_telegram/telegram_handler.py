import html
import logging

import requests


class PylogTelegramHandler(logging.Handler):

    def __init__(self, chat_id, token):
        logging.Handler.__init__(self)

        self.chat_id = chat_id
        self.token = token

    def emit(self, record):
        try:
            message = self.format(record)
            data = {
                'text': message,
                'chat_id': self.chat_id,
                'disable_notification': True
            }

            if getattr(self.formatter, 'parse_mode', None):
                data['parse_mode'] = self.formatter.parse_mode

            url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=self.token)
            requests.request(url=url, method='POST', data=data)

        except:
            self.handleError(record)


class TelegramFormatter(logging.Formatter):
    """Base formatter class suitable for use with `TelegramHandler`"""

    fmt = "%(asctime)s %(levelname)s\n[%(name)s:%(funcName)s]\n%(message)s"
    parse_mode = ''

    def __init__(self, fmt=None, *args, **kwargs):
        super(TelegramFormatter, self).__init__(fmt or self.fmt, *args, **kwargs)


class MarkdownFormatter(TelegramFormatter):
    """Markdown formatter for telegram."""
    fmt = '`%(asctime)s` *%(levelname)s*\n[%(name)s:%(funcName)s]\n%(message)s'
    parse_mode = 'Markdown'

    def formatException(self, *args, **kwargs):
        string = super(MarkdownFormatter, self).formatException(*args, **kwargs)
        return '```python\n%s```' % string


class HtmlFormatter(TelegramFormatter):
    """Html formatter for telegram."""
    fmt = '<i>%(asctime)s</i> <b>%(levelname)s</b>\n[%(name)s:%(funcName)s]\n<code>%(message)s</code>'
    parse_mode = 'HTML'

    def formatMessage(self, record):
        record.funcName = html.escape(record.funcName)
        record.message = html.escape(record.message)
        string = super(HtmlFormatter, self).formatMessage(record)
        return '%s' % string
