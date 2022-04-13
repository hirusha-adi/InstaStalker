import json
import os
import sys


class Database:
    config_filename = os.path.join(os.getcwd(), "config.json")

    if not(os.path.isfile(config_filename)):
        with open(config_filename, "w", encoding="utf-8") as _file:
            _file.write(
                '{\n\t"username": "",\n\t"password": ""\n\t"web": {\n\t\t"host": "0.0.0.0",\n\t\t"port": 8080,\n\t\t"debug": false\n\t}\n}')

    with open(config_filename, "r", encoding="utf-8") as _file:
        _data = json.load(_file)

    USERNAME = _data["username"].strip()
    PASSWORD = _data["password"].strip()

    if USERNAME is None:
        username_file = os.path.join(os.getcwd(), "username.txt")
        if os.path.isfile(username_file):
            with open(username_file, "r", encoding="utf-8") as _uname_file:
                USERNAME = _uname_file.read().strip()
        else:
            sys.exit(
                "No username/email/phone-number is given to log-in. Please fill it in the `config.json` file or have it in the './username.txt' file")

    if PASSWORD is None:
        password_file = os.path.join(os.getcwd(), "password.txt")
        if os.path.isfile(password_file):
            with open(password_file, "r", encoding="utf-8") as _passwd_file:
                PASSWORD = _uname_file.read().strip()
        else:
            sys.exit(
                "No passowrd is given to log-in. Please fill it in the `config.json` file or have it in the './password.txt' file.")

    try:
        HOST: str = _data["web"]["host"]
        if not(len(str(HOST).split(".")) == 4):
            HOST: str = "0.0.0.0"
    except KeyError:
        HOST: str = "0.0.0.0"

    try:
        PORT = _data["web"]["port"]
        try:
            PORT: int = int(PORT)
        except ValueError:
            PORT: int = 8080
    except KeyError:
        PORT: int = 8080

    try:
        DEBUG = _data["web"]["debug"]
        if isinstance(DEBUG, str):
            if DEBUG.lower() in ("true", "t", "yes", "y"):
                DEBUG: bool = True
            else:
                DEBUG: bool = False
        elif isinstance(DEBUG, bool):
            pass
        else:
            DEBUG: bool = False
    except KeyError:
        DEBUG: bool = False
