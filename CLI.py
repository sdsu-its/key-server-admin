import getpass

import App
import Key
import Param
import User


class CLI:
    current_app = ""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_login(self):
        """
        Check if the supplied Username and Password are correct

        :return: Status Code
         :rtype: int
        """
        return User.check_login(self.username, self.password)

    # noinspection PyTypeChecker
    def command(self, c):
        c = c.strip()

        if c == "help":
            print("""Welcome to the Key Server Admin!

** [Verb] [Type] [Optional Param] **
Verbs:
- List    = List out all the specified TYPE
            ex. list app

- Create  = Create a new TYPE
            ex. create user

- Update  = Update a TYPE, the item to modify is
            specified as an additional parameter
            ex. update app test

- Delete  = Delete a TYPE, the item to delete is
            specified as an additional parameter
            ex. delete param url

Types:
- app     = Applications - Act like folders for Parameters
- key     = API Key - used by clients to fetch params
- param   = Parameter, requires an app to be selected
- user    = Admin User


** select [App_Name] **
Select allows you to select an application to work with.
This is required when you want to modify parameters.

** exit **
If an app is currently selected, goes back to home.
If no app is currently selected, quits the admin CLI

** help **
Lists this help info""")

        elif c.lower().__contains__("select"):
            try:
                target_app = c.split(" ")[1]
            except IndexError:
                print("Invalid select condition - please specify which app you want to select")
                return

            if target_app in App.list_apps(self.username, self.password):
                CLI.current_app = target_app
            else:
                print("That is not a valid app name, type 'list apps' to see all the current apps.")

        elif c.lower().__contains__("list"):
            try:
                list_item = c.lower().split(" ")[1]
            except IndexError:
                print("Invalid list condition - please specify what you want to list")
                return

            if list_item.__contains__("-h") or list_item.__contains__("help"):
                print("""List allows you to list out different applications, keys, users, and parameters.

** list [type] **
type `help` to list out all the types and their roles

In order to list parameters, an application needs to be selected.""")

            elif list_item.__contains__("users"):
                for u in User.list_users(self.username, self.password):
                    print("\t%s (%s)" % (u['username'], u['email']))

            elif list_item.__contains__("apps"):
                for a in App.list_apps(self.username, self.password):
                    print("\t" + a)

            elif list_item.__contains__("key"):
                for k in Key.list_keys(self.username, self.password):
                    print ("\t%s (%s)\n"
                           "\t\t Permissions: %s" % (k["application_name"], k["application_key"], k["permissions"]))

            elif list_item.__contains__("param"):
                if CLI.current_app == "":
                    print("Cannot list params when no app is selected")
                else:
                    for p in Param.list_params(self.username, self.password, CLI.current_app):
                        print("\t%s = %s" % (p['name'], p['value']))

            else:
                print("Unknown List Command - type `list -h` or `list help` for help.")

        elif c.lower().__contains__("create"):
            try:
                create_item = c.lower().split(" ")[1]
            except IndexError:
                print("Invalid create condition - please specify what you want to create")
                return

            if create_item.__contains__("-h") or create_item.__contains__("help"):
                print("""Create allows you to create new applications, keys, users, and parameters

** create [type] **
type `help` to list out all the types and their roles

In order to create parameters, an application needs to be selected.""")

            elif create_item.__contains__("user"):
                while True:
                    username = raw_input("\tUsername: ").strip()
                    password = None

                    while True:
                        password = getpass.getpass("\tPassword: ")
                        password_conf = getpass.getpass("\tConfirm Password: ")
                        if password == password_conf:
                            break
                        else:
                            print("Passwords do not match. Try Again.")

                    email = raw_input("\tEmail: ").strip()

                    conf = raw_input("\n\tUsername: %s\n\tPassword: %s\n\tEmail: %s\n\tIs this correct [Y/n]" %
                                     (username, password, email)).strip()

                    if conf.lower() == "y" or conf == "":
                        user = User.create_new(self.username, self.password, username, password, email)
                        print("Created New User: %s" % user["username"])

                        break

            elif create_item.__contains__("app"):
                while True:
                    app_name = raw_input("\tApplication Name: ").strip()

                    conf = raw_input("\n\tApplication Name: %s\n\tIs this correct [Y/n]" % app_name).strip()
                    if conf.lower() == "y" or conf == "":
                        app = App.create_app(self.username, self.password, app_name)
                        print("Created New App: %s" % app["name"])

                        break

            elif create_item.__contains__("key"):
                while True:
                    application_name = raw_input("\tApplication Name: ").strip()
                    print("\tIn case you need a refresher... Application permissions are as follows:\n"
                          "\t\t* use +app_name to whitelist the key for that app\n"
                          "\t\t* use -app_name to blacklist the key for that app\n"
                          "\t\t* use NO to revoke the key\n"
                          "\t\t* or use ALL to grant the key access to all apps")
                    permissions = raw_input("\tApplication Permissions: ").strip()
                    if permissions == "":
                        permissions = "ALL"

                    conf = raw_input("\n\tName: %s\n\tPermissions: %s\n\tIs this correct [Y/n]" % (
                        application_name, permissions)).strip()

                    if conf.lower() == "y" or conf == "":
                        key = Key.create_key(self.username, self.password, application_name, permissions)
                        print("Created New Key: %s" % key["application_key"])

                        break

            elif create_item.__contains__("param"):
                if CLI.current_app == "":
                    print("Cannot create param when no app is selected")
                else:
                    while True:
                        param_name = raw_input("\tParameter Name: ").strip()
                        param_value = raw_input("\tParameter Value: ").strip()

                        conf = raw_input(
                            "\n\tParameter Name: %s\n\tParameter Value: %s\n\tIs this correct [Y/n]" % (param_name,
                                                                                                        param_value)) \
                            .strip()

                        if conf.lower() == "y" or conf == "":
                            param = Param.create_param(self.username, self.password, CLI.current_app, param_name,
                                                       param_value)
                            print("Created New Parameter: %s" % param["parameter_name"])

                            break

            else:
                print("Unknown Create Command - type `create -h` or `create help` for help.")

        elif c.lower().__contains__("update"):
            try:
                update_item = c.lower().split(" ")[1]
            except IndexError:
                print("Invalid update condition - please specify what you want to update")
                return

            try:
                update_item_name = c.split(" ")[2]
            except IndexError:
                print("Invalid update condition - please specify which %s you want to update." % update_item)
                return

            if update_item.__contains__("-h") or update_item.__contains__("help"):
                print("""Update allows you to update existing applications, keys, users, and parameters

** update [type] [username/applicationName/applicationKey/parameterName]**
type `help` to list out all the types and their roles

In order to create parameters, an application needs to be selected.""")

            elif update_item.__contains__("user"):
                user_info = User.list_users(self.username, self.password)
                for u in user_info:
                    if u['username'] == update_item_name:
                        user_info = u
                        break

                while True:
                    password = None
                    while True:
                        password = getpass.getpass("\tNew Password [Leave blank to keep]: ")
                        password_conf = getpass.getpass("\tConfirm New Password: ")
                        if password == password_conf:
                            break
                        else:
                            print("Passwords do not match. Try Again.")

                    email = raw_input("\tEmail [%s]: " % user_info['email']).strip()
                    email = email if email != "" else user_info['email']

                    conf = raw_input("\n\tUsername: %s\n\tPassword: %s\n\tEmail: %s\n\tIs this correct [Y/n]" %
                                     (update_item_name, password, email)).strip()

                    if conf.lower() == "y" or conf == "":
                        user = User.update_user(self.username, self.password, update_item_name, password=password,
                                                email=email)

                        # Updating the current user's password, so let's update the one we are using to login to the API
                        if update_item_name == self.username:
                            self.password = password

                        print("Updated User: %s" % user["username"])

                        break

            elif update_item.__contains__("key"):
                key_info = Key.list_keys(self.username, self.password)
                for k in key_info:
                    if k['application_key'] == update_item_name:
                        key_info = k
                        break

                while True:
                    application_name = raw_input("\tApplication Name [%s]: " % key_info['application_name'])
                    permissions = raw_input("\tPermissions [%s]: " % key_info['permissions'])

                    conf = raw_input("\n\tName: %s\n\tPermissions: %s\n\tIs this correct [Y/n]" % (
                        application_name, permissions)).strip()

                    if conf.lower() == "y" or conf == "":
                        key = Key.update_key(self.username, self.password, update_item_name,
                                             application_name=application_name,
                                             permissions=permissions)
                        print("Updated Key: %s" % key['application_key'])

                        break

            elif update_item.__contains__("param"):
                if CLI.current_app == "":
                    print("Cannot update param when no app is selected")
                else:
                    while True:
                        param_value = raw_input("\tNew Value Value: ").strip()

                        conf = raw_input("\n\tParameter Value: %s\n\tIs this correct [Y/n]" % param_value).strip()

                        if conf.lower() == "y" or conf == "":
                            param = Param.create_param(self.username, self.password, CLI.current_app, update_item_name,
                                                       param_value)
                            print("Updated Parameter: %s" % param["name"])

                            break
            else:
                print("Unknown Update Command - type `update -h` or `update help` for help.")

        elif c.lower().__contains__("delete"):
            try:
                delete_item = c.lower().split(" ")[1]
            except IndexError:
                print("Invalid delete condition - please specify what you want to delete")
                return

            try:
                delete_item_name = c.split(" ")[2]
            except IndexError:
                print("Invalid delete condition - please specify which %s you want to delete." % delete_item)
                return

            if delete_item.__contains__("-h") or delete_item.__contains__("help"):
                print("""Delete allows you to remove applications, users, and parameters.
Delete revokes keys, which is the only delete action that can be undone; to
reactivate a revoked key, update the permissions of the key.

** update [type] [username/applicationName/applicationKey/parameterName]**
type `help` to list out all the types and their roles

In order to create parameters, an application needs to be selected.""")

            elif delete_item.__contains__("user"):
                conf = raw_input("\n\tUsername to remove: %s\n\tIs this correct [Y/n]" % delete_item_name).strip()

                if conf.lower() == "y" or conf == "":
                    status = User.delete_user(self.username, self.password, delete_item_name)
                    if status:
                        print("User was deleted Successfully")
                    else:
                        print("Problem deleting user, check server logs for details")

            elif delete_item.__contains__("app"):
                conf = raw_input("\n\tApplication to remove: %s\n\tIs this correct [Y/n]" % delete_item_name).strip()

                if conf.lower() == "y" or conf == "":
                    status = App.delete_app(self.username, self.password, delete_item_name)
                    if status:
                        print("App was deleted Successfully")
                    else:
                        print("Problem deleting app, check server logs for details")

            elif delete_item.__contains__("key"):
                conf = raw_input("\n\tKey to remove: %s\n\tIs this correct [Y/n]" % delete_item_name).strip()

                if conf.lower() == "y" or conf == "":
                    status = Key.delete_key(self.username, self.password, delete_item_name)
                    if status:
                        print("Key was Revoked Successfully - to reactivate the Key, update its permissions")
                    else:
                        print("Problem revoking key, check server logs for details")

            elif delete_item.__contains__("param"):
                if CLI.current_app == "":
                    print("Cannot delete param when no app is selected")
                else:
                    conf = raw_input("\n\tParam to remove: %s\n\tIs this correct [Y/n]" % delete_item_name).strip()

                    if conf.lower() == "y" or conf == "":
                        status = Param.delete_param(self.username, self.password, CLI.current_app, delete_item_name)
                        if status:
                            print("Param was deleted Successfully")
                        else:
                            print("Problem deleting param, check server logs for details")

            else:
                print("Unknown Delete Command - type `delete -h` or `delete help` for help.")

        elif c.lower().__contains__("exit"):
            if CLI.current_app == "":
                exit(0)
            else:
                CLI.current_app = ""

        else:
            print("Command not recognized")
