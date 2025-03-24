# Ansible Collection - itential.toolkit
This ansible project is intended to be a toolkit for operators of Itential
Automation Platform and Itential Automation Gateway. It includes Itential's
recommended methods for performing administration tasks, making adminstrative
changes to the platforms, and interrogating dependent systems for runtime
information.

## Connection Variables

Playbooks in this collection need to connect to some combination of:
- **Host Machines** (via SSH), or
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

Example:
`ansible-playbook playbook.yml -i hosts.yaml --extra-vars 'platform_auth_token=<token>'`

# Tools

1. [Get Platform Token](#get-platform-token)
2. [Restart Adapter](#restart-adapter)
3. [Metrics](#metrics)
4. [Adjusting Adapters' log level](#adjusting-adapters'-log-level)
5. [Starting/Stopping Workersics](#starting/stopping-workers)
6. [Mongo Dump](#mongo-dump)
7. [Create Adapter](#create-adapter)
8. [App Adapter Version](#app-adapter-version)
9. [Sync IAG Custom Script Schema](#sync-iag-custom-script-schema)
10. [Dependencies Version](#dependencies-version)
11. [Switch Active Profile](#switch-active-profile)
12. [Job and Task Worker Status](#job-and-task-worker-status)
13. [RBAC Settings](#rbac-settings)
14. [IAG Refresh Custom Script](#iag-refresh-custom-script)
15. [Restart Platform](#restart-platform)
16. [Restart IAG](#restart-iag)
17. [Admin All Roles](#admin-all-roles)

## Get Platform Token
This tool will fetch a platform session token and display it to the screen.
This playbook requries Platform API access.

### Example
`ansible-playbook playbooks/get_platform_token.yml -i hosts.yaml --extra-vars 'platform_username=<some-user> platform_password=<some-password>'`

## Restart Adapter
This tool will restart a list of provided adapter names after fetching an IAP
session token. This playbook requries Platform API access.

### Required Variables

| NAME              | DESCRIPTION                                       |
|-------------------|---------------------------------------------------|
| adapters          | String(one adapter) or Comma separated list of adapter names to restart  |

### Example
`ansible-playbook playbooks/restart_adapters.yml -i hosts.yaml --extra-vars 'iap_username=<some-user> iap_password=<some-password> adapters=<comma-separated-list-of-adapter-names>'`

## Metrics
This tool will show the quantity of workflows, templates, MOP templates, 
analytic templates, JSTs, JSON forms, forms, jobs and automations in IAP. 
This playbook requries Platform API access.

### Example
`ansible-playbook playbooks/metrics.yml -i hosts.yaml --extra-vars 'iap_username=<some-user> iap_password=<some-password>'`

## Adjusting Adapters' log level
This tool will adjust the log level of the adapters in IAP. Available options are 
`error, warn, info, debug, trace, spam`. This playbook requries Platform API access.

### Required Variables

| NAME         | DESCRIPTION                                                     |
|--------------|-----------------------------------------------------------------|
| log_level    | The log level to be set (error, warn, info, debug, trace, spam) |

### Example
`ansible-playbook playbooks/adapters_log_level.yml -i hosts.yaml --extra-vars 'iap_username=<some-user> iap_password=<some-password> log_level=error'`

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
`ansible-playbook start_task_worker.yml -i hosts.yaml --extra-vars 'platform_username=<user> platform_password=<password>'`


## Mongo Dump
This tool will dump single or all collections from a given mongo database. 
This playbook requries Host Machine access.

### Required Variables

| NAME           | DESCRIPTION                                                              |
|----------------|--------------------------------------------------------------------------|
| db             | The database containing collections to be dumped                         |
| mongo_auth_db  | The database to perform authentication on                                |
| mongo_username | MongoDB username                                                         |
| mongo_password | MongoDB user's password                                                  |
| collection     | Optional. If not defined, all collections in the database will be dumped |

### Example
`ansible-playbook playbooks/mongo_dump.yml -i hosts.yaml --extra-vars 'db=itential collection=workflows'`

## Create Adapter
This tool will create the adapter and starts it.
This playbook requries Platform API access.

### Required Variables

| NAME                    | DESCRIPTION                                                                                 |
|-------------------------|---------------------------------------------------------------------------------------------|
| adapter_properties_file | Name of the JSON file where the adapter properties are stored.                              |

### Example
`ansible-playbook playbooks/create_adapter.yml -i hosts --extra-vars 'adapter_properties_file="<file_path>" iap_username=<some-user> iap_password=<some-password>'`

## App Adapter Version
This tool will show the the version of applications and adapters in the IAP. User can specify the applications/adapters of which they want to see the version. The users also have the option to view the versions of all applications and adapters.
This playbook requries Platform API access.

### Required Variables

| NAME              | DESCRIPTION                                                                                 |
|-------------------|---------------------------------------------------------------------------------------------|
| adapter_app_names | Names of applications and adapters, separated by comma. If no names are provided, will return versions of all applications and adapters.|

### Example
The following command returns the version of local_aaa adapter and AGManager application:

`ansible-playbook playbooks/app_adapter_version.yml -i hosts --extra-vars 'adapter_app_names="local_aaa, AGManager" iap_username=<some-username> iap_password=<some-password>'`

The following command returns the version of all applications and adapters.

`ansible-playbook playbooks/app_adapter_version.yml -i hosts --extra-vars 'adapter_app_names="" iap_username=<some-username> iap_password=<some-password>'`


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
This playbook requries Host Machine access.

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

## Switch Active Profile
This tool will switch the active profile to the profile specified. After the active profile is switched, it restarts the IAP. This playbook requries Host Machine and Platform API access.

### Required Variables

| NAME         | DESCRIPTION                                     |
|--------------|-------------------------------------------------|
| id           | The id of the profile.                          |

### Example
`ansible-playbook playbooks/app_adapter_version.yml -i hosts --extra-vars 'id=<profile-id> iap_username=<some-username> iap_password=<some-password>'`

Running the playbook by providing ssh key file from command line

`ansible-playbook playbooks/app_adapter_version.yml -i hosts --extra-vars 'id=<profile-id> iap_username=<some-username> iap_password=<some-password>' --private-key <key_file_name>`

Running the playbook by providing ssh username and password from command line

`ansible-playbook playbooks/app_adapter_version.yml -i hosts --extra-vars 'id=<profile-id> iap_username=<some-username> iap_password=<some-password>' -u <ssh_username> --ask-pass <password>`


## Job and Task Worker Status
This tool will return the status of job worker and task worker of IAP.
This playbook requries Platform API access.

### Required Variables

| NAME              | DESCRIPTION                                                                                 |
|-------------------|---------------------------------------------------------------------------------------------|
| iap_port          | The port that the IAP is running on.                                                        |
| iap_protocol      | The HTTP/HTTPS protocol that is being used by IAP                                           |
| iap_username      | The application user's name                                                                 |
| iap_password      | The application user's password                                                             |

### Example
`ansible-playbook playbooks/job_worker_status.yml -i hosts --extra-vars 'iap_username=<some-username> iap_password=<some-password>`

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
`ansible-playbook rbac_settings.yml -i hosts.yaml --extra-vars 'platform_username=<user> platform_password=<password> users=["user1","user2"]'`


## IAG Refresh Custom Script
This tool will refresh the custom scripts cache in IAG. Furthermore, it also restarts the AGManager application and the IAG adapters in the IAP so that the updated scripts can be accessed from the IAP. The IAP hostnames should be under `platform` group and the IAG hostnames should be under the `gateway` group inside the host file.
This playbook requries Platform API and IAG API access.

### Example
`ansible-playbook playbooks/iag_refresh_custom_scripts.yml -i hosts --extra-vars 'iap_username=<some-username> iap_password=<some-password> iag_username=<some-username> iag_password=<some-password>'`

## Restart Itential Platform
This tool will perform a safe restart the Itential Platform. It turns off task and job workers then waits until there are no
in progress jobs before restarting the Platform. The playbook requires Host Machine and Platform API access.

### Example
Running playbook when password/key file is defined in the hosts file

`ansible-playbook playbooks/restart_iap.yml -i hosts`

## Restart IAG
This tool will restart the IAG.
This playbook requries Host Machine access.

### Example
Running playbook when password/key file is defined in the hosts file

`ansible-playbook playbooks/restart_iag.yml -i hosts`

Running playbook by providing key file from command-line

`ansible-playbook playbooks/restart_iag.yml -i hosts --private-key <key_file_name>`

Running playbook by providing username and password from command-line

`ansible-playbook playbooks/restart_iag.yml -i hosts -u <ssh_username> --ask-pass <password>`


## Admin All Roles
This tool will add all available roles to the admin user.
This playbook requries Platform API access.

### Example
`ansible-playbook playbooks/admin_all_roles.yml -i hosts.yaml --extra-vars 'iap_username=<some-user>' --vault-password-file .password`