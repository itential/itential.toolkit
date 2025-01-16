from ansible.module_utils.basic import AnsibleModule
import requests

DOCUMENTATION = r'''
---
module: iap_check_active_tasks
short_description: Check the number of active tasks for an IAP host.
description:
  - This module uses the IAP APIs to check the number of active "running" tasks on an IAP host.
  - It supports both HTTP and HTTPS protocols.
  - In addition to providing the number of active tasks, it also returns a list of all running tasks.
options:
  platform_base_url:
    description:
      - The base URL of the IAP server, including protocol, hostname, and port.
      - Example: http://iap.example.com:3000
    required: true
    type: str
  token:
    description:
      - A valid session token for authentication.
    required: true
    type: str
    no_log: true

author:
  - Wade Stern <wade.stern@itential.com>
'''

EXAMPLES = r'''
- name: Check active tasks
  iap_check_active_tasks:
    platform_base_url: "http://iap.example.com:3000"
    token: "abc123"
  register: result

- debug:
    msg: "Number of active tasks: {{ result.active_tasks }}"
    
- debug:
    msg: "Active tasks: {{ result.tasks }}"
'''

RETURN = r'''
active_tasks:
  description: The number of active tasks on the IAP host.
  type: int
  returned: always
tasks:
  description: A list of details for all active tasks on the IAP host.
  type: list
  returned: always
'''

def main():
    module_args = dict(
        platform_base_url=dict(type='str', required=True),
        token=dict(type='str', required=True, no_log=True)
    )

    result = dict(
        changed=False,
        active_tasks=0,
        tasks=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    platform_base_url = module.params['platform_base_url']
    token = module.params['token']

    url = f"{platform_base_url}/operations-manager/tasks"

    params = {
        "equals[status]": "running"
    }

    headers = {
        'Cookie': f"token={token}"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
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
