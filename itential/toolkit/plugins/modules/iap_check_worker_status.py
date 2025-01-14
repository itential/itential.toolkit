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
- name: Check the status of jobs and tasks workers
  iap_workers_status:
    hostname: "iap.example.com"
    port: 3000
    https: false
    token: "abc123"
  register: result

- debug:
    msg: "Workers status: {{ result.status }}"
'''

RETURN = r'''
status:
  description: The status of jobs and tasks workers returned by the API.
  type: dict
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
        status={}
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
    url = f"{protocol}://{hostname}:{port}/workflow_engine/workers/status"

    headers = {
        'Cookie': f"token={token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse and return the response
        result['status'] = response.json()
        module.exit_json(**result)

    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"Failed to retrieve workers status: {str(e)}")

if __name__ == '__main__':
    main()
