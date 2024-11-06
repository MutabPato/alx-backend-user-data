#!/usr/bin/env python3
"""
Personal data
"""


from typing import List
import re
import logging


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Returns the log message obfuscated
    """
    for f in fields:
        message = re.sub(
                f'{f}=.*?{separator}', f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        """constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records"""
        record.msg = filter_datum(
                self.fields, self.REDACTION, record.
                getMessage(), self.SEPARATOR)

        return super(RedactingFormatter, self).format(record)
