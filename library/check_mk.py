#!/usr/bin/python
# -*- coding: utf-8 -*-


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '0.1'}

DOCUMENTATION = '''
---
module: check_mk
short_description: Talk to check_mk API
description:
    - Used to add, edit, and delete hosts via check_mk web API.
    - Service discovery and changeset activation is also implemented.
version_added: "0.2"
author: "Fabian Weisshaar (@elnappo)"
options:
    server_url:
        description:
            - URL of check_mk server, with protocol (http or https).
        required: true
        default: null

    username:
        description:
            - Check_mk username, used to authenticate against the server.
        required: true
        default: null

    secret:
        description:
            - Check_mk user secret.
        required: true
        default: null

    hostname:
        description:
            -  Name of the host in check_mk.
        required: false
        default: null

    folder:
        description:
            - Description of the options goes here.
        required: false
        default: ""

    state:
        description:
            - Description of the options goes here.
        required: false
        default: present
        choices:
          - present
          - absent

    discover_services:
        description:
            - Description of the options goes here.
        required: false
        default: null
        choices:
          - new
          - remove
          - fixall
          - refresh

    activate_changes:
        description:
            - Description of the options goes here.
        required: false
        default: no

    attributes:
        description:
            - Description of the options goes here.
        required: false
        default: {}

    validate_certs:
        description:
            - Verify SSL certificate or not
        required: false
        default: True

notes:
    - Other things consumers of your module should know.

requirements:
    - requests >= 2.5.0
'''

EXAMPLES = '''
- name: Add host to monitoring
  check_mk:
    hostname: {{ inventory_hostname }}
    folder: os/linux
    state: present
  delegate_to: localhost
  notify: check_mk activate changes

- name: Add host to monitoring and discover services
  check_mk:
    hostname: {{ inventory_hostname }}
    folder: dfd-inf
    discover_services: refresh
    state: present
  delegate_to: localhost
  notify: "check_mk activate changes"

- name: Remove host from monitoring
  check_mk:
    hostname: {{ inventory_hostname }}
    state: absent
  delegate_to: localhost
  notify: "check_mk activate changes"

handlers:
  - name: check_mk activate changes
    check_mk: activate_changes=all
'''

RETURN = '''
dest:
    description: destination file/path
    returned: success
    type: string
    sample: /path/to/file.txt
'''
from ansible.module_utils.basic import AnsibleModule
from distutils.version import LooseVersion
import json

try:
    import requests

    REQUESTS_FOUND = True
except ImportError:
    REQUESTS_FOUND = False


class CheckMKAPI(object):
    def __init__(self, ansible_module):
        self._module = ansible_module
        self._api_url = self._module.params["server_url"] + "check_mk/webapi.py?_username=%s&_secret=%s" % (self._module.params["username"], self._module.params["secret"])
        self._session = requests.Session()

        if not self._module.params["server_url"].endswith("/"):
            self._module.fail_json(msg="Server URL must end with / e.g. http://cmk.example.com/monitoring/")

    def _api_request(self, action, payload=None, fail_on_error=True):
        try:
            r = self._session.post(self._api_url + action, data=payload or {}, verify=self._module.params["validate_certs"])
            r.raise_for_status()
            if r.json()["result_code"] != 0 and fail_on_error:
                self._module.fail_json(msg=r.json()["result"])
            return r.json()["result"]
        except getattr(json.decoder, 'JSONDecodeError', ValueError):
            self._module.fail_json(msg=r.text, http_status_code=r.status_code, payload=payload)
        except requests.exceptions.RequestException as err:
            self._module.fail_json(msg=str(err), payload=payload)

    def get_host_attributes(self, hostname):
        return self._api_request("&action=get_host&effective_attributes=1", {'hostname': hostname})

    def add_host(self, hostname, folder, attributes=None):
        payload = {'hostname': hostname, "folder": folder.lower(), 'attributes': attributes or {}}
        return self._api_request("&action=add_host", "request="+json.dumps(payload))

    def edit_host(self, hostname, attributes=None, unset_attributes=None):
        payload = {"attributes": attributes, "hostname": hostname, "unset_attributes": unset_attributes or []}
        return self._api_request("&action=edit_host","request="+json.dumps(payload))

    def delete_host(self, hostname):
        return self._api_request("&action=delete_host", {'hostname': hostname})

    def discover_services(self, hostname, mode="new"):
        return self._api_request("&action=discover_services&mode=%s" % mode, {'hostname': hostname})

    def activate_changes(self, mode="dirty"):
        return self._api_request("&action=activate_changes&mode=%s" % mode)

    def host_exists(self, hostname):
        return self._api_request("&action=get_host&effective_attributes=1", {'hostname': hostname},
                                 False) != "Check_MK exception: No such host"


def main():
    argument_spec = dict(
        server_url=dict(type="str", required=True),
        username=dict(type="str", required=True, ),
        secret=dict(type="str", required=True, no_log=True),

        hostname=dict(type="str"),
        folder=dict(type="str", default=""),
        attributes=dict(type="dict", default={}),
        state=dict(type="str", choices=['present', 'absent'], default="present"),
        validate_certs=dict(type="bool", default=True),

        discover_services=dict(type="str", choices=['new', 'remove', 'fixall', 'refresh']),
        activate_changes=dict(type="bool")
    )
    a_module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if not REQUESTS_FOUND:
        a_module.fail_json(msg='requests library is required for this module')

    if requests.__version__ and LooseVersion(requests.__version__) < LooseVersion('2.5.0'):
        a_module.fail_json(msg='requests library version should be >= 2.5.0')

    cmk = CheckMKAPI(a_module)
    result = dict(changed=False)

    # add / delete host
    if a_module.params["hostname"]:
        host_exists = cmk.host_exists(a_module.params["hostname"])

        if a_module.params["state"] == "present" and not host_exists:
            result["changed"] = True
            result["addhost"] = cmk.add_host(a_module.params["hostname"], a_module.params["folder"], a_module.params["attributes"])

        if a_module.params["state"] == "absent" and host_exists:
            result["changed"] = True
            cmk.delete_host(a_module.params["hostname"])

    # Adjust attributes
    if a_module.params["hostname"] and host_exists and  a_module.params["attributes"]:
        result["changed"] = True
        result["edit_host"] = cmk.edit_host(a_module.params["hostname"], a_module.params["attributes"])

    # discover services
    if a_module.params["discover_services"]:
        if not a_module.params["hostname"]:
            a_module.fail_json(msg='Hostname is required when using discover_services')

        result["changed"] = True
        result["discover_services"] = cmk.discover_services(a_module.params["hostname"], a_module.params["discover_services"])

    # activate changes
    if a_module.params["activate_changes"]:
        if result["changed"] == True:
           result["activate_changes"] = cmk.activate_changes()

    a_module.exit_json(**result)


if __name__ == '__main__':
    main()
