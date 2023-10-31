import sys
from logging import getLogger
from os import environ

COMMAND_HANDLER = environ.get("COMMAND_HANDLER", "! /").split()
