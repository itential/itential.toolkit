#!/usr/bin/python

# Copyright: (c) 2024, Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: iap_rbac_processing

short_description: Processes RBAC data for users in Itential IAP.

version_added: "1.0.0"

description:
    - Filters authorization accounts for specified users.
    - Retrieves and formats assigned roles.
    - Returns structured user-role mappings and a formatted message.

options:
    auth_accounts:
        description: List of authorization accounts retrieved from IAP.
        required: true
        type: list

    roles_response:
        description: List of roles retrieved from IAP.
        required: true
        type: list

    users:
        description: List of users to process.
        required: true
        type: list

author:
    - Itential, Inc
'''

EXAMPLES = r'''
- name: Process RBAC data for a specific user
  itential.platform.iap_rbac_processing:
    auth_accounts: "{{ auth_accounts.json.results }}"
    roles_response: "{{ roles_response.json.results }}"
    users: "admin"
  register: rbac_results

- name: Process RBAC data for multiple users
  itential.platform.iap_rbac_processing:
    auth_accounts: "{{ auth_accounts.json.results }}"
    roles_response: "{{ roles_response.json.results }}"
    users: ["admin", "operator"]
  register: rbac_results

- name: Display formatted RBAC message
  debug:
    msg: "{{ rbac_results.formatted_message.split('\n') }}"
'''

RETURN = r'''
    users_roles:
        description: List of users with their assigned roles.
        type: list
        returned: always
        sample:
            - username: "admin"
              roles: ["AdapterModels.admin", "AGManager.admin"]
            - username: "unknown_user"
              roles: ["User not found"]

    formatted_message:
        description: Readable RBAC role assignments for each user.
        type: str
        returned: always
        sample: |
            Roles assigned for admin at 127.0.0.1:
            AdapterModels.admin, AGManager.admin

            Roles assigned for unknown_user at 127.0.0.1:
            User not found
'''
