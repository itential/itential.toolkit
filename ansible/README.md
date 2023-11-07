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

>ansible-playbook -i hosts adapterRestart.yml
