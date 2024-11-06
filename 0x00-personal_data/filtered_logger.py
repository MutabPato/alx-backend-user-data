#!/usr/bin/env python3
"""
Personal data
"""


from typing import List
import re


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Returns the log message obfuscated
    """
    for f in fields:
        message = re.sub(
                f'{f}=.*?{separator}', f'{f}={redaction}{separator}', message)
    return message
