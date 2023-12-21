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