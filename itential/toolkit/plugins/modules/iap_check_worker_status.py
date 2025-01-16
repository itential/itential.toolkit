from ansible.module_utils.basic import AnsibleModule
import requests

DOCUMENTATION = r'''
---
module: iap_check_worker_status
short_description: Check the status of the jobs and tasks workers in IAP.
description:
  - This module uses the IAP APIs to check the status of the jobs and tasks workers.
  - It supports both HTTP and HTTPS protocols.
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

author:
  - Wade Stern <wade.stern@itential.com>
'''

EXAMPLES = r'''
- name: Check the status of jobs and tasks workers
  iap_workers_status:
    platform_base_url: "http://iap.example.com:3000"
    token: "abc123"
  register: result
'''

RETURN = r'''
status:
  description: The status of jobs and tasks workers returned by the API.
  type: dict
  returned: always
'''

def main():
    module_args = dict(
        platform_base_url=dict(type='str', required=True),
        token=dict(type='str', required=True, no_log=True)
    )

    result = dict(
        changed=False,
        status={}
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    platform_base_url = module.params['platform_base_url']
    token = module.params['token']

    url = f"{platform_base_url}/workflow_engine/workers/status"

    headers = {
        'Cookie': f"token={token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result['status'] = response.json()
        module.exit_json(**result)

    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"Failed to retrieve workers status: {str(e)}")

if __name__ == '__main__':
    main()
