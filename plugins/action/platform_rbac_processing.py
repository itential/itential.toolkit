# Copyright (c) 2022, Itential, LLC
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# Generates a list of roles assigned to each user provided in the users parameter.
# Example:
# - name: Process RBAC Data
#   itential.toolkit.platform_rbac_processing:
#     auth_accounts: "{{ auth_accounts.json.results }}"
#     roles_response: "{{ roles_response.json.results }}"
#     users: "{{ users }}"
#   register: rbac_results

from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):
        """Main entry point for processing RBAC data."""
        
        module_args = self._task.args

        # Extract parameters
        auth_accounts = module_args.get('auth_accounts', [])
        roles_response = module_args.get('roles_response', [])
        users = module_args.get('users')

        # Retrieve the IP address or default to inventory hostname
        ip_address = task_vars.get("ansible_host", task_vars.get("inventory_hostname", "unknown"))

        # Validate input types
        if not isinstance(auth_accounts, list) or not isinstance(roles_response, list):
            return {
                "failed": True,
                "msg": "Both 'auth_accounts' and 'roles_response' must be lists."
            }

        # Validate and normalize `users`
        if not users:
            return {
                "failed": True,
                "msg": "The 'users' parameter must be provided and cannot be empty."
            }
        if isinstance(users, str):
            users = [users]
        elif not isinstance(users, list):
            return {"failed": True, "msg": "The 'users' parameter must be a list or a string."}

        # Create lookup for roles
        roles_dict = {
            role["_id"]: f"{role['provenance']}.{role['name']}"
            for role in roles_response
        }

        # Create lookup for accounts
        account_lookup = {acc["username"]: acc for acc in auth_accounts}

        # Process users and roles
        users_roles = []
        for user in users:
            if user in account_lookup:
                acc = account_lookup[user]
                role_ids = (
                    [role["roleId"] for role in acc.get("assignedRoles", [])] +
                    [role["roleId"] for role in acc.get("inheritedRoles", [])]
                )
                assigned_roles = [
                    roles_dict[role_id] for role_id in role_ids if role_id in roles_dict
                ]
            else:
                assigned_roles = ["User not found"]

            users_roles.append({"username": user, "roles": assigned_roles})

        # Generate formatted message
        formatted_message = "\n".join(
            f"Roles assigned for {user['username']} at {ip_address}:\n{', '.join(user['roles'])}"
            for user in users_roles
        )

        return {
            "changed": False,
            "users_roles": users_roles,
            "formatted_message": formatted_message
        }
