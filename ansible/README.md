**Overview:**

Ansible playbook to start/stop an IAP adapter or application by name.

**Usage:**

Edit the required service variables in the host.yml file. 
>Valid service_types are 'applications' and 'adapters'.

Example:

    service_name: Jst
    service_type: applications
    action: stop
    username: admin@pronghorn
    password: admin

Run Playbook:

>ansible-playbook -i hosts serviceRestart.yml



## Running the Metrics Playbook

1. Execute the following command to run the Ansible playbook.

    ```bash
    ansible-playbook -i hosts metrics.yml
    ```

2. Review output: The playbook will show the count of workflows, templates, jobs etc.