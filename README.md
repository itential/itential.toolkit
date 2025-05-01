# Ansible Collection - itential.toolkit
This ansible project is intended to be a toolkit for operators of Itential
Automation Platform and Itential Automation Gateway. It includes Itential's
recommended methods for performing administration tasks, making adminstrative
changes to the platforms, and interrogating dependent systems for runtime
information.

## Connection Variables

Playbooks in this collection need to connect to some combination of:
- **Ansible Hosts** (via SSH), or
- The **Itential Platform Service** (via API).
- The **IAG Service** (via API).

### Ansible Connection Variables
To connect to the instances using Ansible:
- `ansible_user`: The SSH username.
- One of the following authentication methods:
  - `ansible_password`: SSH password *(can be prompted with `--ask-pass`)*.
  - `ansible_ssh_private_key_file`: Path to SSH private key *(can be passed with `--private-key`)*.

### Itential Platform API Connection Variables
To connect to the Itential Platform API, provide 
- `platform_port`: The port that platform is accessible on
- `platform_https`: Boolean that describes HTTPS (`true`) or HTTP (`false`) for the Platform API.
- Either:
    - `platform_username` and `platform_password`, **or**
    - `platform_auth_token`.

### IAG API Connection Variables
To connect to the IAG API, provide 
- `iag_port`: The port that IAG is accessible on
- `iag_https`: Boolean that describes HTTPS (`true`) or HTTP (`false`) for the IAG API.
- Either:
    - `iag_username` and `iag_password`, **or**
    - `iag_auth_token`.

### Providing Variables
Variables can be:
- Defined in an **inventory file (hosts file)**.
- Passed via the command line using `--extra-vars` or `-e`.
- Encoded using ansible vault and provided by either of the above methods.

Example:
`ansible-playbook playbook.yml -i hosts.yaml --extra-vars 'platform_auth_token=<token>'`

# Tools

1. [Get Platform Token](#get-platform-token)
2. [Restart Adapters](#restart-adapters)
3. [Metrics](#metrics)
4. [Adjusting Adapters' Log Level](#adjusting-adapters-log-level)
5. [Starting/Stopping Workers](#startingstopping-workers)
6. [Sync IAG Custom Script Schema](#sync-iag-custom-script-schema)
7. [Dependencies Version](#dependencies-version)
8. [Job and Task Worker Status](#job-and-task-worker-status)
9. [RBAC Settings](#rbac-settings)
10. [IAG Refresh Custom Scripts](#iag-refresh-custom-scripts)
11. [Restart Platform](#restart-platform)
12. [Restart IAG](#restart-iag)
13. [IAG Fakenos](#iag-fakenos)
14. [MongoDB Change Password](#mongodb-change-password)
15. [Redis Change Password](#redis-change-password)
16. [Sentinel Change Password](#sentinel-change-password)
17. [Step Down Mongo Primary](#step-down-mongo-primary)
18. [Step Down Redis Primary](#step-down-redis-primary)


## Get Platform Token
This tool will fetch a platform session token and display it to the screen.
This playbook requries Platform API access.

### Example
`ansible-playbook playbooks/get_platform_token.yml -i hosts.yaml --extra-vars 'platform_username=<some-user> platform_password=<some-password>'`

## Restart Adapters
This tool will restart a list of provided adapter names after fetching an IAP
session token. This playbook requries Platform API access.

### Required Variables

| NAME              | DESCRIPTION                                       |
|-------------------|---------------------------------------------------|
| adapters          | Comma separated list of adapter names to restart  |

### Example
`ansible-playbook playbooks/restart_adapters.yml -i hosts.yaml adapters=<comma-separated-list-of-adapter-names>'`

## Metrics
This tool will show the quantity of workflows, templates, MOP templates, 
analytic templates, JSTs, JSON forms, forms, jobs and automations in IAP. 
This playbook requries Platform API access.

### Example
`ansible-playbook playbooks/metrics.yml -i hosts.yaml`

## Adjusting Adapters' log level
This tool will adjust the log level of the adapters in IAP. Available options are 
`error, warn, info, debug, trace, spam`. This playbook requries Platform API access.

### Required Variables

| NAME         | DESCRIPTION                                                     |
|--------------|-----------------------------------------------------------------|
| log_level    | The log level to be set (error, warn, info, debug, trace, spam) |
| adapters     | Comma separated list of adapters to update                      |

### Example
`ansible-playbook playbooks/adapters_log_level.yml -i hosts.yaml --extra-vars log_level=error'`

## Starting/Stopping Workers
These playbooks will start or stop **task workers** and/or **job workers** (supported in Platform 2023.1 and later).
These playbooks requrie Platform API access.

### Playbooks
Each action has its own playbook:
- `start_task_worker.yml`
- `stop_task_worker.yml`
- `start_job_worker.yml`
- `stop_job_worker.yml`

### Example Usage
`ansible-playbook start_task_worker.yml -i hosts.yaml`

## Sync IAG Custom Script Schema
This tool will grab the JSON schema(decorations) of the custom script from the first IAG host in the `gateway` group and applies it to the custom script across other IAG hosts in the `gateway` group.
This playbook requries IAG API access.

### Required Variables

| NAME              | DESCRIPTION                                                                                 |
|-------------------|---------------------------------------------------------------------------------------------|
| script_name       | Name of the custom script                                                                   |

> **_NOTE:_**  Make sure that the first host in the `gateway` group has the latest JSON schema.

### Example
`ansible-playbook sync_iag_script_schema.yml -i hosts --extra-vars 'script_name=hello.py'`

## Dependencies Version
This tool will return the version of redis, rabbitmq, mongobd, IAP components, and IAG components. More information about the dependencies can be found in [this](https://docs.itential.com/docs/itential-dependencies-consolidated) page. The rabbitmq server, redis server, IAP server and IAG server
should be under their respective group in the hosts file.
This playbook requries ansible host access.

### Required Variables

| NAME         | DESCRIPTION                                                                           |
|--------------|---------------------------------------------------------------------------------------|
| component   | The component(mongodb, redis, etc) to target to. Available options are:                |
|              |  `mongodb` : Returns the version of mongodb                                           |
|              |  `redis` : Returns the version of redis                                               |
|              |  `rabbitmq` : Returns the version of rabbitmq                                         |
|              |  `platform` : Returns the version of mongodb, redis, rabbitmq, and IAP dependencies   |
|              |  `gateway` : Returns the version of IAG dependencies.                                 |
|              |  `all` : Returns the version across all five components.                              | 

### Example
`ansible-playbook playbooks/dependencies_version.yml -i hosts --extra-vars 'component=all'`

## Job and Task Worker Status
This tool will return the status of job worker and task worker of IAP.
This playbook requries Platform API access.

### Example
`ansible-playbook playbooks/job_worker_status.yml -i hosts`

## RBAC Settings
This playbook retrieves **RBAC (Role-Based Access Control)** settings for one or more users in the Platform. It gathers authorization accounts and roles from the Platform API, processes the data, and displays the assigned roles for the specified users.
This playbook requries Platform API access.

### Required Variables

| NAME                | DESCRIPTION                                                                |
|---------------------|----------------------------------------------------------------------------|
| users               | A single username (string) or a list of usernames.                         |

---

### Example Usage

Get RBAC settings for multiple users using username/password:
`ansible-playbook rbac_settings.yml -i hosts.yaml --extra-vars users=["user1","user2"]'`

## IAG Refresh Custom Script
This tool will refresh the custom scripts cache in IAG. Furthermore, it also restarts the AGManager application and the IAG adapters in the IAP so that the updated scripts can be accessed from the IAP. The IAP hostnames should be under `platform` group and the IAG hostnames should be under the `gateway` group inside the host file.
This playbook requries Platform API and IAG API access.

### Example
`ansible-playbook playbooks/iag_refresh_custom_scripts.yml -i hosts --extra-vars 'iap_username=<some-username> iap_password=<some-password> iag_username=<some-username> iag_password=<some-password>'`

## Restart Itential Platform
This tool will perform a safe restart the Itential Platform. It turns off task and job workers then waits until there are no
in progress jobs before restarting the Platform. The playbook requires ansible host and Platform API access.

### Example
Running playbook when password/key file is defined in the hosts file

`ansible-playbook playbooks/restart_platform.yml -i hosts`

## Restart IAG
This tool will restart the IAG.
This playbook requries ansible host access.

### Example
Running playbook when password/key file is defined in the hosts file

`ansible-playbook playbooks/restart_iag.yml -i hosts`

Running playbook by providing key file from command-line

`ansible-playbook playbooks/restart_iag.yml -i hosts --private-key <key_file_name>`

Running playbook by providing username and password from command-line

`ansible-playbook playbooks/restart_iag.yml -i hosts -u <ssh_username> --ask-pass <password>`

## IAG Fakenos
This tool will install and start fakenos which will create mock devices on an IAG host.
The playbook requires ansible host access.

### Required Variables

| NAME             | DESCRIPTION                                                     |
|------------------|-----------------------------------------------------------------|
| fakenos_devices  | Object containing the device type. Each device type needs vendor, platform, and count      |


### Example Inventory variable

```
fakenos_devices:
  cisco_ios:
    vendor: cisco
    platform: ios
    count: 5
  juniper_junos:
    vendor: junipernetworks
    platform: junos
    count: 5
```

### Example

Running playbook when fakenos_devices is defined in the inventory file

`ansible-playbook rbac_settings.yml -i hosts.yaml`

## Mongodb Change Password
This tool will update the password for the 'itential' user in the mongo database.
It also updates the platform configuration and restarts the platform.
The playbook requires ansible host access for mongo and platform.

| NAME             | DESCRIPTION                                                     |
|------------------|-----------------------------------------------------------------|
| mongo_admin_password  | the password for the 'admin' user in the mongo database      |
| mongo_new_password  | The new password for the itential user                        |

### Example
`ansible-playbook mongodb_change_password.yml -i hosts.yaml --extra-vars "mongo_admin_password=password mongo_new_password=newpassword"`

## Redis Change Password
This tool will update the password for the 'itential' user in the Redis configuration file.
It also updates the platform configuration and restarts the platform.
The playbook requires ansible host access for redis and platform.

| NAME             | DESCRIPTION                                                     |
|------------------|-----------------------------------------------------------------|
| redis_new_password  | The new password for the itential user                       |

### Example
`ansible-playbook redis_change_password.yml -i hosts.yaml --extra-vars "redis_new_password=newpassword"`

## Sentinel Change Password
This tool will update the password for the 'sentineluser' user in the Redis and Sentinel configuration files.
It also updates the platform configuration and restarts the platform.
The playbook requires ansible host access for redis and platform.

| NAME             | DESCRIPTION                                                     |
|------------------|-----------------------------------------------------------------|
| sentinel_new_password  | The new password for the sentineluser user                |

### Example
`ansible-playbook sentinel_change_password.yml -i hosts.yaml --extra-vars "sentinel_new_password=newpassword"`

## Step Down Mongo Primary
This tool forces a mongo re-election for a new Mongo Primary.
The playbook requires ansible host access for mongodb.

| NAME             | DESCRIPTION                                                     |
|------------------|-----------------------------------------------------------------|
| mongo_admin_password | The password for the admin user in the mongodb              |

### Example
`ansible-playbook stepdown_mongo_primary.yml -i hosts.yaml --extra-vars "mongo_admin_password=password"`

## Step Down Redis Primary
This tool forces a redis re-election for a new Redis Primary.
The playbook requires ansible host access for redis

| NAME             | DESCRIPTION                                                     |
|------------------|-----------------------------------------------------------------|
| redis_password   | The password for the admin user in redis             |

### Example
`ansible-playbook stepdown_redis_primary.yml -i hosts.yaml --extra-vars "redis_password=password"`

# Roles

## Auth Token
This role retrieves and stores the auth token from the platform API. It is used in playbooks that need
to make many api requests so that ansible doesn't have to re-authenticate each time it wants to make a request.
This role requires platform API access

## Restart Adapters
This role makes an API call to restart all of the adapters from the 'adapter_names' list.
It requires platform API access

## Restart Platform
This role contains the logic to do a safe restart of the platform. It includes a handler that can be
used when the role is imported. This role does not contain a main task file, so to run it the restart.yml
task file or the handler must be explicitly called.
This role requires platform API access