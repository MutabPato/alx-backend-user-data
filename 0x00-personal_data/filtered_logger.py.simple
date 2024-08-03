#!/usr/bin/env python3
""" Regex-ing """

import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    for field in fields:
        regex = rf'{field}=(.*?){separator}'
        message = re.sub(regex, f'{field}={redaction}{separator}', message)
    return message
