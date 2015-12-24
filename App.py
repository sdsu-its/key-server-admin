import os

import packages.requests as requests


def list_apps(username, password):
    """
    List Applications

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: str
    :return: List of all Applications
     :rtype: list
    """
    apps = requests.get(os.getenv("key_server_site") + "/rest/app/list", auth=(username, password))

    try:
        assert apps.status_code == 200

        return_lists = list()
        for app in apps.json():
            return_lists.append(app["name"])

        return return_lists
    except AssertionError:
        exit("Problem Listing Apps (Check Server Logs for Details) - HTTP Status: %i" % apps.status_code)


def create_app(username, password, application_name):
    """
    Create Application

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: str
    :param application_name: Application Name to Create
     :type application_name: str
    :return: List of all Applications
     :rtype: dict
    """
    app = requests.post(os.getenv("key_server_site") + "/rest/app/create",
                        auth=(username, password),
                        json={"name": application_name})

    try:
        assert app.status_code == 201

        return app.json()
    except AssertionError:
        exit("Problem Creating App (Check Server Logs for Details) - HTTP Status: %i" % app.status_code)


def delete_app(username, password, application_name):
    """
    Delete Application

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: Admin Password
    :param application_name: Application Name to Delete
     :type application_name: str
    :return: If the App was deleted successfully
     :rtype: bool
    """
    app = requests.delete(os.getenv("key_server_site") + "/rest/app/delete",
                          auth=(username, password),
                          json={"name": application_name})

    return app.status_code == 202
