# Copyright (C) 2022, Pyronear.

# This program is licensed under the Apache License version 2.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0.txt> for full license details.

import os

from dotenv import load_dotenv

__all__ = ["API_URL", "API_LOGIN", "API_PWD"]

# If there is an .env, load it
load_dotenv()

DEBUG: bool = os.environ.get("DEBUG", "") != "False"
API_URL: str = os.environ.get("API_URL", "")
API_LOGIN: str = os.environ.get("API_LOGIN", "")
API_PWD: str = os.environ.get("API_PWD", "")
CACHE_FOLDER: str = ".cache"
