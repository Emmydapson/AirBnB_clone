#!/usr/bin/python3
""" init for class FileStorage """

from models.engine import file_storage

storage = file_storage.FileStorage()
storage.reload()
