#!/usr/bin/env python3
""" Regex-ing """

import re
from typing import List


def filter_datum(fields: List[str], redaction:
                 str,  message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        regex = rf'{field}=(.*?){separator}'
        message = re.sub(regex, f'{field}={redaction}{separator}', message)
    return message
