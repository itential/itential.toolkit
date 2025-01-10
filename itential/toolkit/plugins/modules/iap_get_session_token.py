from ansible.module_utils.basic import AnsibleModule
import requests
import base64

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
  hostname:
    description:
      - Hostname or IP address of the IAP server.
    required: true
    type: str
  port:
    description:
      - Port on which the IAP server is running.
    required: true
    type: int
  https:
    description:
      - Whether to use HTTPS for the connection.
    required: true
    type: bool

author:
  - Your Name <wade.stern@itential.com>
'''

EXAMPLES = r'''
- name: Retrieve IAP session token
  iap_get_session_token:
    username: "admin"
    password: "mypassword"
    hostname: "iap.example.com"
    port: 3000
    https: false
  register: result

- debug:
    msg: "Session token is {{ result.token }}"
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
        hostname=dict(type='str', required=True),
        port=dict(type='int', required=True),
        https=dict(type='bool', required=True)
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
    hostname = module.params['hostname']
    port = module.params['port']
    https = module.params['https']

    protocol = 'https' if https else 'http'
    url = f"{protocol}://{hostname}:{port}/login"

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

        # Attempt to decode Base64-encoded response
        raw_response = response.text.strip()  # Remove extra whitespace
        try:
            decoded_token = base64.b64decode(raw_response).decode('utf-8')
            result['token'] = decoded_token
        except (base64.binascii.Error, UnicodeDecodeError):
            module.fail_json(msg=f"Unexpected response: {raw_response}")

        module.exit_json(**result)

    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"Failed to retrieve session token: {str(e)}")


if __name__ == '__main__':
    main()
