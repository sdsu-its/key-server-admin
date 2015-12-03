import os

import packages.requests as requests


def list_params(username, password, application_name):
    """
    List Parameters

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: str
    :param application_name: Application Name to which the Parameter is Associated
     :type application_name: str
    :return: List of all parameters
     :rtype: list
    """
    params = requests.get(os.getenv("key_server_site") + "/rest/param/list?app=" + application_name,
                          auth=(username, password))

    try:
        assert params.status_code == 200

        return params.json()
    except AssertionError:
        exit("Problem listing Params (Check Server Logs for Details) - HTTP Status: %i" % params.status_code)


def create_param(username, password, application_name, param_name, param_value):
    """
    Create new Parameter

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type username: str
    :param application_name: Application Name to which the Parameter is Associated
     :type application_name: str
    :param param_name: Parameter Name
     :type param_name: str
    :param param_value: Parameter Value
     :type param_value: str
    :return: New Param
     :rtype: dict
    """
    param = requests.post(os.getenv("key_server_site") + "/rest/param/create?app=" + application_name,
                          auth=(username, password),
                          json={
                              "name": param_name,
                              "value": param_value
                          })
    try:
        assert param.status_code == 201

        return param.json()
    except AssertionError:
        exit("Problem Creating Param (Check Server Logs for Details) - HTTP Status: %i" % param.status_code)


def update_param(username, password, application_name, param_name, param_value):
    """
    Update Parameter

    :param username: Admin Username
     :type username: str
    :param password: Admin Password
     :type password: str
    :param application_name: Application Name to which the Parameter is Associated
     :type application_name: str
    :param param_name: Parameter Name
     :type param_name: str
    :param param_value: New Parameter Value
     :type param_value: str
    :return: Updated Param
     :rtype: dict
    """
    param = requests.put(os.getenv("key_server_site") + "/rest/param/update?app=" + application_name,
                         auth=(username, password),
                         json={
                             "name": param_name,
                             "value": param_value
                         })
    try:
        assert param.status_code == 202

        return param.json()
    except AssertionError:
        exit("Problem Updating Param (Check Server Logs for Details) - HTTP Status: %i" % param.status_code)


def delete_param(username, password, application_name, param_name):
    """
    Delete Parameter

    :param username: Admin Username
     :type  username: str
    :param password: Admin Password
     :type password: str
    :param application_name: Application Name to which the Parameter is Associated
     :type application_name: str
    :param param_name: Parameter Name
     :type param_name: str
    :return: If the parameter was deleted
     :rtype: bool
    """
    param = requests.delete(os.getenv("key_server_site") + "/rest/param/delete?app=" + application_name,
                            auth=(username, password),
                            json={
                                "name": param_name})

    return param.status_code == 202
