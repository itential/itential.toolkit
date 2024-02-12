# Ansible Collection - itential.toolkit
This ansible project is intended to be a toolkit for operators of Itential
Automation Platform and Itential Automation Gateway. It includes Itential's
recommended methods for performing administration tasks, making adminstrative
changes to the platforms, and interrogating dependent systems for runtime
information.

# Tools

## Get IAP Token
This tool will fetch an IAP session token and display it to the screen. It
requires the following variables, these should be defined in the hosts file,
as "extra-vars" on the command line, or a mixture of both. For example, the
password  may not be approrpriate to keep in a hosts file and may be better
suited for the command line.

| NAME         | DESCRIPTION                                       |
|--------------|---------------------------------------------------|
| iap_port     | The HTTP port that the application is running on. |
| iap_protocol | The HTTP protocol that is being used by IAP       |
| iap_username | The application user's name                       |
| iap_password | The application user's password                   |

### Example
`ansible-playbook playbooks/get_iap_token.yml -i hosts.yaml --extra-vars 'iap_username=<some-user> iap_password=<some-password>'`

## Restart Adapter
This tool will restart a list of provided adapter names after fetching an IAP
session token. It requires the following variables, these should be defined in
the hosts file, as "extra-vars" on the command line, or a mixture of both. For
example, the password  may not be approrpriate to keep in a hosts file and may
be better suited for the command line.

| NAME         | DESCRIPTION                                       |
|--------------|---------------------------------------------------|
| iap_port     | The HTTP port that the application is running on. |
| iap_protocol | The HTTP protocol that is being used by IAP       |
| iap_username | The application user's name                       |
| iap_password | The application user's password                   |
| adapters     | Comma separated list of adapter names to restart  |

### Example
`ansible-playbook playbooks/restart_adapters.yml -i hosts.yaml --extra-vars 'iap_username=<some-user> iap_password=<some-password> adapters=<comma-separated-list-of-adapter-names>'`

## Metrics
This tool will show the quantity of workflows, templates, MOP templates, 
analytic templates, JSTs, JSON forms, forms, jobs and automations in IAP. 
It requires the following variables, these should be defined in
the hosts file, as "extra-vars" on the command line, or a mixture of both. For
example, the password  may not be approrpriate to keep in a hosts file and may
be better suited for the command line.

| NAME         | DESCRIPTION                                       |
|--------------|---------------------------------------------------|
| iap_port     | The HTTP port that the application is running on. |
| iap_protocol | The HTTP protocol that is being used by IAP       |
| iap_username | The application user's name                       |
| iap_password | The application user's password                   |

### Example
`ansible-playbook playbooks/metrics.yml -i hosts.yaml --extra-vars 'iap_username=<some-user> iap_password=<some-password>'`

## Adjusting Adapters' log level
This tool will adjust the log level of the adapters in IAP. Available options are 
`error, warn, info, debug, trace, spam`.
It requires the following variables, these should be defined in
the hosts file, as "extra-vars" on the command line, or a mixture of both. For
example, the password  may not be approrpriate to keep in a hosts file and may
be better suited for the command line.

| NAME         | DESCRIPTION                                                     |
|--------------|-----------------------------------------------------------------|
| iap_port     | The HTTP port that the application is running on.               |
| iap_protocol | The HTTP protocol that is being used by IAP                     |
| iap_username | The application user's name                                     |
| iap_password | The application user's password                                 |
| log_level    | The log level to be set (error, warn, info, debug, trace, spam) |

### Example
`ansible-playbook playbooks/adapters_log_level.yml -i hosts.yaml --extra-vars 'iap_username=<some-user> iap_password=<some-password> log_level=error'`

## Starting/Stopping Workers
This tool will start or stop task worker and/or job worker (2023.1 and later) in IAP.
It requires the following variables, these should be defined in
the hosts file, as "extra-vars" on the command line, or a mixture of both. For
example, the password  may not be approrpriate to keep in a hosts file and may
be better suited for the command line.

| NAME         | DESCRIPTION                                            |
|--------------|--------------------------------------------------------|
| iap_port     | The HTTP port that the application is running on.      |
| iap_protocol | The HTTP protocol that is being used by IAP            |
| iap_username | The application user's name                            |
| iap_password | The application user's password                        |
| iap_action   | The desired action to perform. Available options are:  |
|              |  'start_task_worker'                                   |
|              |  'stop_task_worker'                                    |
|              |  'start_job_worker'                                    |
|              |  'stop_job_worker'                                     |
|              |  'start_both'                                          |
|              |  'stop_both'                                            | 

### Example
`ansible-playbook playbooks/workers.yml -i hosts.yaml --extra-vars 'iap_username=<some-user> iap_password=<some-password> iap_action=start_task_worker'`

## Mongo Dump
This tool will dump single or all collections from a given mongo database. 
It requires the following variables, these should be defined in
the hosts file, as "extra-vars" on the command line, or a mixture of both. For
example, the password  may not be approrpriate to keep in a hosts file and may
be better suited for the command line.

| NAME           | DESCRIPTION                                                              |
|----------------|--------------------------------------------------------------------------|
| db             | The database containing collections to be dumped                         |
| mongo_auth_db  | The database to perform authentication on                                |
| mongo_username | MongoDB username                                                         |
| mongo_password | MongoDB user's password                                                  |
| collection     | Optional. If not defined, all collections in the database will be dumped |

### Example
`ansible-playbook playbooks/mongo_dump.yml -i hosts.yaml --extra-vars 'db=itential collection=workflows'`

## App Adapter Version
This tool will show the the version of applications and adapters in the IAP. User can specify the applications/adapters of which they want to see the version. The users also have the option to view the versions of all applications and adapters.
It requires the following variables, these should be defined in
the hosts file, as "extra-vars" on the command line, or a mixture of both. For
example, the password  may not be approrpriate to keep in a hosts file and may
be better suited for the command line.

| NAME              | DESCRIPTION                                                                                 |
|-------------------|---------------------------------------------------------------------------------------------|
| iap_port          | The port that the IAP is running on.                                                        |
| iap_protocol      | The HTTP/HTTPS protocol that is being used by IAP                                           |
| iap_username      | The application user's name                                                                 |
| iap_password      | The application user's password                                                             |
| adapter_app_names | Names of applications and adapters, separated by comma. If no names are provided, will return versions of all applications and adapters.|

### Example
The following command returns the version of local_aaa adapter and AGManager application:

`ansible-playbook playbooks/app_adapter_version.yml -i hosts --extra-vars 'adapter_app_names="local_aaa, AGManager" iap_username=<some-username> iap_password=<some-password>'`

The following command returns the version of all applications and adapters.

`ansible-playbook playbooks/app_adapter_version.yml -i hosts --extra-vars 'adapter_app_names="" iap_username=<some-username> iap_password=<some-password>'`


## RBAC Settings
This tool will return the roles assigned for a list of users in IAP.
It requires the following variables, these should be defined in
the hosts file, as "extra-vars" on the command line, or a mixture of both. For
example, the password  may not be approrpriate to keep in a hosts file and may
be better suited for the command line.

| NAME              | DESCRIPTION                                                                                 |
|-------------------|---------------------------------------------------------------------------------------------|
| iap_port          | The port that the IAP is running on.                                                        |
| iap_protocol      | The HTTP/HTTPS protocol that is being used by IAP                                           |
| iap_username      | The application user's name                                                                 |
| iap_password      | The application user's password                                                             |
| users             | Usernames, seperated by comma.                                                              |

### Example
`ansible-playbook playbooks/rbac_settings.yml -i hosts --extra-vars 'iap_username=<some-username> iap_password=<some-password> users=<username1>,<username2>'`
