from ansible.module_utils.basic import AnsibleModule
import requests

DOCUMENTATION = r'''
---
module: iap_check_active_tasks
short_description: Check the number of active tasks for an IAP host.
description:
  - This module uses the IAP APIs to check the number of active "running" tasks on an IAP host.
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

author:
  - Wade Stern <wade.stern@itential.com>
'''

EXAMPLES = r'''
- name: Check active tasks
  iap_check_active_tasks:
    hostname: "iap.example.com"
    port: 3000
    https: false
    token: "abc123"
  register: result
'''

RETURN = r'''
active_tasks:
  description: The number of active tasks on the IAP host.
  type: int
  returned: always
'''

def main():
    module_args = dict(
        hostname=dict(type='str', required=True),
        port=dict(type='int', required=True),
        https=dict(type='bool', required=True),
        token=dict(type='str', required=True, no_log=True)
    )

    result = dict(
        changed=False,
        active_tasks=0
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    hostname = module.params['hostname']
    port = module.params['port']
    https = module.params['https']
    token = module.params['token']

    protocol = 'https' if https else 'http'
    base_url = f"{protocol}://{hostname}:{port}/operations-manager/tasks"

    params = {
        "equals[status]": "running"
    }

    headers = {
        'Cookie': f"token={token}"
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()

        # Parse the response JSON
        tasks_response = response.json()
        if "data" in tasks_response and isinstance(tasks_response["data"], list):
            result['active_tasks'] = len(tasks_response["data"])
            result['tasks'] = tasks_response["data"]
        else:
            module.fail_json(msg="Unexpected response format", response=tasks_response)

        module.exit_json(**result)

    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"Failed to retrieve active tasks: {str(e)}")

if __name__ == '__main__':
    main()
