# upgrade-tools
This repo contains a collection of tools that can be used when performing IAP and IAG upgrades.


## Getting started
1. Clone this repo
2. `npm install` the dependencies
3. Run the tools

## Tools

### validate-all-workflows
This tool can be used to validate all workflows found in an IAP. It mimics the same behavior as when you save a workflow in the UI. It will generate a report of all errors and warnings per workflow. It uses IAP APIs and therefore needs to be able to access a running IAP instance. It also requires a username of an active user in order to obtain an IAP session token. The script will prompt for a password which is masked.

Usage:
`node validate-all-workflows.js <iap-host-port> <iap-username>`

Example:
`node validate-all-workflows.js http://127.0.0.1:3000 admin@pronghorn`

