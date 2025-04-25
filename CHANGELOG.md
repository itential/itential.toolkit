# Changelog

## v1.0.3 (April 25, 2025)

* Added readmes to all roles
* fix lint

Full Changelog: https://github.com/itential/itential.toolkit/compare/v1.0.2...v1.0.3 


## v1.0.2 (April 25, 2025)

* Update galaxy version and changelog for release 1.0.2 [skip ci]

Full Changelog: https://github.com/itential/itential.toolkit/compare/v1.0.1...v1.0.2 


## v1.0.1 (April 25, 2025)

* Added files needed to push collection to galaxy and added galaxy dependencies to ansible lint action
* added empty line eof
* update url to match renamed repo

Full Changelog: https://github.com/itential/itential.toolkit/compare/v1.0.0...v1.0.1 


## v1.0.0 (April 18, 2025)

* Added a module that can fetch the iap session token.
* Added block for restart sentinel handler
* Added explanation to role variable
* Added nolog to tasks that would debug passwords added delegate to localhost to api calls in restart_platform
* Added note about mongo_url and mongo_password to file.
* Added note about vault.
* Added note to use vault for sensitive data.
* Added playbook to change the mongo password. Refactored restart_platform To separate the api calls from the restart task. This was necessary since changing passwords will cause the platform to go down and the api to become unavailable.
* Added playbook to force mongo to elect a new primary.
* Added playbook to force the mongo primary to step down
* Added redis secondary and platform secondary.
* Added stepdown redis primary
* Changed name of plugin from iap to platform
* Changed rbac settings to use a action plugin instead of ansible code. removed delegate to localhost from action plugin module calls. Added unit tests for new rbac action plugin.
* Create ansible-lint.yml
* Create pylint.yml
* Create pytest.yml
* Created playbook to change password for Sentinel.
* Created redis_change_password playbook.
* Do not decode the api key
* Fixed logic that detects if the itential user exists.
* Fixed terminology in documentation
* Flatten project structure by removing itential/toolkit folder
* Got rid of become true.
* Got rid of delegate to localhost
* Included Name in documentation template
* Initial commit
* Made collection ansible lint compliant
* Modified to use ansible community module
* Refactored restart platform role to use handlers. modified mongodb_change_password and redis_change_password playbooks.
* Removed unusable files
* Reworked restart_adapters and split workers into different playbooks for each function.
* Tweaked adapters log level, turned restart adapters into role.
* Tweaked some lines so that they fall below 100 character limit.
* Tweaked variables
* Updated readme and added new playbooks and roles
* Updated test to use new platform filenames
* Updated to fit format of other password change playbooks
* added admin_all_roles  https://github.com/itential/itential.toolkit/pull/1
* added ansible galaxy role paths
* added connection local to playbooks
* added note about ansible vault in documentation
* added platform_secondary and redis_secondary to redis and mongo change passwords.
* added requirements file
* added tag to deactivate workers
* added tag to the deactivate workers task so that it can be skipped if the api is unavailable
* added unused workflow script  https://github.com/itential/itential.toolkit/pull/2
* ansible lint
* init
* removed requirements
* tasks/main is not needed to call handlers
* testing
* testing ansible lint file tweaks
* testing noqa
* tweaks to fix lint
* updated rbac settings and restart iap to use itential platform modules. got rid of old plugin
* wrong rbac file

