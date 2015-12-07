import base64
import os

import packages.requests as requests


def check_login(username, password):
    """
    Check User Credentials

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: str
    :return: If credentials are valid
     :rtype: bool
    """

    r = requests.get(os.getenv("key_server_site") + "/rest/user/verify", auth=(username, password))
    return r.status_code == 200


def list_users(username, password):
    """
    List Users

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: str
    :return: List of all Users
     :rtype: list
    """
    users = requests.get(os.getenv("key_server_site") + "/rest/user/list", auth=(username, password))

    try:
        assert users.status_code == 200

        return users.json()
    except AssertionError:
        exit("Problem listing Users (Check Server Logs for Details) - HTTP Status: %i" % users.status_code)


def create_new(admin_username, admin_password, username, password, email):
    """
    Create a new User

    :param admin_username: Admin Username
     :type admin_username: str
    :param admin_password: Admin Password
     :type admin_password: str
    :param username: Username for new User
     :type username: str
    :param password: Password for New User
     :type password: str
    :param email: Email Address for New User
     :type email: str
    :return: New User
     :rtype: dict
    """
    user = requests.post(os.getenv("key_server_site") + "/rest/user/create",
                         auth=(admin_username, admin_password),
                         json={"username": username,
                               "password": base64.b64encode(password),
                               "email": email})

    try:
        assert user.status_code == 201

        return user.json()
    except AssertionError:
        exit("Problem creating new user (Check Server Logs for Details) - HTTP Status: %i" % user.status_code)


def update_user(admin_username, admin_password, username, password=None, email=None):
    """
   Update a User

   :param admin_username: Admin Username
    :type admin_username: str
   :param admin_password: Admin Password
    :type admin_password: str
   :param username: Username for User
    :type username: str
   :param password: New Password for User
    :type password: str
   :param email: New Email Address for User
    :type email: str
   :return: Updated User
    :rtype: dict
   """

    if password is not None:
        password = base64.b64encode(password)

    user = requests.put(os.getenv("key_server_site") + "/rest/user/update",
                        auth=(admin_username, admin_password),
                        json={"username": username,
                              "password": password,
                              "email": email})

    try:
        assert user.status_code == 202

        return user.json()
    except AssertionError:
        exit("Problem updating user (Check Server Logs for Details) - HTTP Status: %i" % user.status_code)


def delete_user(admin_username, admin_password, username):
    """
    Delete User

    :param admin_username: Admin Username
     :type admin_username: str
    :param admin_password: Admin Password
     :type admin_password: str
    :param username: Username to delete
     :type username: str
    :return: If the user was deleted successfully
     :rtype: bool
    """
    user = requests.delete(os.getenv("key_server_site") + "/rest/user/delete",
                           auth=(admin_username, admin_password),
                           json={"username": username})

    return user.status_code == 202
