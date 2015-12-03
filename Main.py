import getpass
import json
import os

from CLI import CLI

try:
    with open("config.json") as config_file:
        config_params = json.loads(config_file.read())
        os.environ["key_server_site"] = config_params['site_name']
except IOError:
    print("Config File not found...")
    os.environ["key_server_site"] = ""
except KeyError:
    print("Config File Malformed...")
    os.environ["key_server_site"] = ""

if os.environ["key_server_site"] == "":
    while True:
        site_name = raw_input("Key Server Path: ")
        if site_name[-1] == "/":
            site_name = site_name[:-1]

        sn_conf = raw_input("Is this Correct? [y/n] ")

        if sn_conf.lower() == "y":
            os.environ["key_server_site"] = site_name
            with open("config.json", "w") as config_file:
                config_file.write(json.dumps({'site_name': site_name}))
                print("Config Saved\n\n")

            break

print("Key Server Admin")
user_name = raw_input("Username: ").strip().lower()

user_pass = getpass.getpass("Password: ").lower()

cli = CLI(user_name, user_pass)

if not cli.check_login() == 4:
    exit("Login info is not correct.")

while True:
    command = raw_input("%s > " % (CLI.current_app if CLI.current_app != "" else "~"))
    cli.command(command)
