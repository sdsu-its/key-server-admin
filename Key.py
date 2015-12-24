import os

import packages.requests as requests


def list_keys(username, password):
    """
    List all API Keys

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: str
    :return: List of all API Keys
     :rtype: list
    """
    keys = requests.get(os.getenv("key_server_site") + "/rest/key/list", auth=(username, password))

    try:
        assert keys.status_code / 100 == 2
        return keys.json()

    except AssertionError:
        exit("Problem Listing Keys (Check Server Logs for Details) - HTTP Status: %i" % keys.status_code)


def create_key(username, password, application_name, permissions):
    """
    Create API Key

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: str
    :param application_name: Name of the Application that will be using the API Key
     :type application_name: str
    :param permissions: Permissions for the API Key
     :type permissions: str
    :return: Generated API Key
     :rtype: dict
    """
    key = requests.post(os.getenv("key_server_site") + "/rest/key/issue",
                        auth=(username, password),
                        json={"application_name": application_name,
                              "permissions": permissions})

    try:
        assert key.status_code == 201
        return key.json()
    except AssertionError:
        exit("Problem Creating Key (Check Server Logs for Details) - HTTP Status: %i" % key.status_code)


def update_key(username, password, application_key, application_name=None, permissions=None):
    """
    Update API Key

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: str
    :param application_key: Application Key to Update
     :type application_key: str
    :param application_name: New Application Name
     :type application_name: str
    :param permissions: New Application Permissions
     :type permissions: str
    :return: Updated API Key
     :rtype: dict
    """
    key = requests.put(os.getenv("key_server_site") + "/rest/key/update",
                       auth=(username, password),
                       json={"application_key": application_key,
                             "application_name": application_name,
                             "permissions": permissions})

    try:
        assert key.status_code == 202
        return key

    except AssertionError:
        exit("Problem Updating Key (Check Server Logs for Details) - HTTP Status: %i" % key.status_code)


def delete_key(username, password, application_key):
    """
    Delete API Key

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: str
    :param application_key: Application Key to Delete
     :type application_key: str
    :return: If the Key was revoked
     :rtype: bool
    """
    key = requests.delete(os.getenv("key_server_site") + "/rest/key/revoke",
                          auth=(username, password),
                          json={"application_key": application_key})

    return key.status_code == 202
