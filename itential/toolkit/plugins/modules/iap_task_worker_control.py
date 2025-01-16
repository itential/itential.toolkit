from ansible.module_utils.basic import AnsibleModule
import requests

DOCUMENTATION = r'''
---
module: iap_task_worker_control
short_description: Control the task workers for an IAP host.
description:
  - This module activates or deactivates the task workers on an IAP host using the IAP APIs.
  - It uses the `platform_base_url` to determine the endpoint URL.
options:
  platform_base_url:
    description:
      - Base URL of the IAP server, including protocol, hostname, and port.
    required: true
    type: str
  token:
    description:
      - A valid session token for authentication.
    required: true
    type: str
    no_log: true
  action:
    description:
      - The action to perform on the task workers ("activate" or "deactivate").
    required: true
    type: str
    choices:
      - activate
      - deactivate

author:
  - Wade Stern <wade.stern@itential.com>
'''

EXAMPLES = r'''
- name: Activate task workers
  iap_task_worker_control:
    platform_base_url: "http://iap.example.com:3000"
    token: "abc123"
    action: activate

- name: Deactivate task workers
  iap_task_worker_control:
    platform_base_url: "https://iap.example.com:3000"
    token: "def456"
    action: deactivate
'''

RETURN = r'''
message:
  description: Confirmation message about the performed action.
  type: str
  returned: always
'''

def main():
    module_args = dict(
        platform_base_url=dict(type='str', required=True),
        token=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=['activate', 'deactivate'])
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    platform_base_url = module.params['platform_base_url']
    token = module.params['token']
    action = module.params['action']

    endpoint = f"/workflow_engine/{action}"
    url = f"{platform_base_url}{endpoint}"

    headers = {
        'Cookie': f"token={token}"
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()

        result['changed'] = True
        result['message'] = f"Task workers successfully {action}d."
        module.exit_json(**result)

    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"Failed to {action} task workers: {str(e)}")

if __name__ == '__main__':
    main()
