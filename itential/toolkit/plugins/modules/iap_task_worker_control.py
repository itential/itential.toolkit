from ansible.module_utils.basic import AnsibleModule
import requests

DOCUMENTATION = r'''
---
module: iap_task_worker_control
short_description: Control the task workers for an IAP host.
description:
  - This module activates or deactivates the task workers on an IAP host using the IAP APIs.
  - It supports both HTTP and HTTPS protocols.
options:
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
    hostname: "iap.example.com"
    port: 3000
    https: false
    token: "abc123"
    action: activate

- name: Deactivate task workers
  iap_task_worker_control:
    hostname: "iap.example.com"
    port: 3000
    https: true
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
        hostname=dict(type='str', required=True),
        port=dict(type='int', required=True),
        https=dict(type='bool', required=True),
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

    hostname = module.params['hostname']
    port = module.params['port']
    https = module.params['https']
    token = module.params['token']
    action = module.params['action']

    protocol = 'https' if https else 'http'
    endpoint = f"/workflow_engine/{action}"
    url = f"{protocol}://{hostname}:{port}{endpoint}"

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
