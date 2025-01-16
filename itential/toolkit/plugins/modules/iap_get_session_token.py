from ansible.module_utils.basic import AnsibleModule
import requests

DOCUMENTATION = r'''
---
module: iap_get_session_token
short_description: Retrieve a session token from a running IAP server.
description:
  - This module uses IAP APIs to authenticate and retrieve a session token.
  - It supports both HTTP and HTTPS protocols.
options:
  username:
    description:
      - Username for authentication.
    required: true
    type: str
  password:
    description:
      - Password for authentication.
    required: true
    type: str
    no_log: true
  platform_base_url:
    description:
      - Base URL of the IAP server, including protocol, hostname, and port.
    required: true
    type: str

author:
  - Wade Stern <wade.stern@itential.com>
'''

EXAMPLES = r'''
- name: Retrieve IAP session token
  iap_get_session_token:
    username: "admin"
    password: "mypassword"
    platform_base_url: "http://iap.example.com:3000"
  register: result
'''

RETURN = r'''
token:
  description: The session token retrieved from the IAP server.
  type: str
  returned: always
'''

def main():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        platform_base_url=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        token=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    username = module.params['username']
    password = module.params['password']
    platform_base_url = module.params['platform_base_url']

    url = f"{platform_base_url}/login"

    headers = {'Content-Type': 'application/json'}
    payload = {
        "user": {
            "username": username,
            "password": password
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result['token'] = response.text.strip()

        module.exit_json(**result)

    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"Failed to retrieve session token: {str(e)}")

if __name__ == '__main__':
    main()
