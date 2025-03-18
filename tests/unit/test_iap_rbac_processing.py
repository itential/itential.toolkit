import pytest
from unittest.mock import MagicMock
from ansible_collections.itential.toolkit.plugins.action.iap_rbac_processing import ActionModule


@pytest.fixture
def module_args():
    """Provides a default set of module arguments."""
    return dict(
        auth_accounts=[
            {
                "username": "admin",
                "assignedRoles": [{"roleId": "role1"}],
                "inheritedRoles": [{"roleId": "role2"}]
            },
            {
                "username": "operator",
                "assignedRoles": [{"roleId": "role3"}],
                "inheritedRoles": []
            }
        ],
        roles_response=[
            {"_id": "role1", "provenance": "AdapterModels", "name": "admin"},
            {"_id": "role2", "provenance": "AGManager", "name": "admin"},
            {"_id": "role3", "provenance": "AutomationCatalog", "name": "user"}
        ],
        users=["admin"]
    )


@pytest.fixture
def mock_action_module():
    """Creates an instance of the ActionModule with required dependencies mocked."""
    return ActionModule(
        task=MagicMock(),
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock(),
    )


@pytest.fixture
def default_task_vars():
    """Provides default task variables (mock inventory)."""
    return {"ansible_host": "127.0.0.1"}


def run_module(mock_action_module, module_args, task_vars):
    """Helper function to run the action module with provided args and task_vars."""
    mock_action_module._task.args = module_args
    return mock_action_module.run(task_vars=task_vars)


def test_valid_user(mock_action_module, module_args, default_task_vars):
    """Test that a valid user gets correct roles."""
    module_args["users"] = ["admin"]
    result = run_module(mock_action_module, module_args, default_task_vars)

    expected_message = (
        "Roles assigned for admin at 127.0.0.1:\n"
        "AdapterModels.admin, AGManager.admin"
    )
    assert result["users_roles"] == [{
        "username": "admin",
        "roles": ["AdapterModels.admin", "AGManager.admin"]
    }]
    assert result["formatted_message"] == expected_message


def test_user_not_found(mock_action_module, module_args, default_task_vars):
    """Test handling of a user not found in auth_accounts."""
    module_args["users"] = ["unknown_user"]
    result = run_module(mock_action_module, module_args, default_task_vars)

    expected_message = "Roles assigned for unknown_user at 127.0.0.1:\nUser not found"

    assert result["users_roles"] == [{"username": "unknown_user", "roles": ["User not found"]}]
    assert result["formatted_message"] == expected_message


def test_mixed_users(mock_action_module, module_args, default_task_vars):
    """Test scenario where some users exist, and some do not."""
    module_args["users"] = ["admin", "unknown_user"]
    result = run_module(mock_action_module, module_args, default_task_vars)

    expected_message = (
        "Roles assigned for admin at 127.0.0.1:\nAdapterModels.admin, AGManager.admin\n"
        "Roles assigned for unknown_user at 127.0.0.1:\nUser not found"
    )

    assert result["users_roles"] == [
        {"username": "admin", "roles": ["AdapterModels.admin", "AGManager.admin"]},
        {"username": "unknown_user", "roles": ["User not found"]}
    ]
    assert result["formatted_message"] == expected_message


def test_users_as_string(mock_action_module, module_args, default_task_vars):
    """Test handling when users input is a single string instead of a list."""
    module_args["users"] = "admin"  # Single string instead of list
    result = run_module(mock_action_module, module_args, default_task_vars)

    expected_message = (
        "Roles assigned for admin at 127.0.0.1:\n"
        "AdapterModels.admin, AGManager.admin"
    )

    assert result["users_roles"] == [{
        "username": "admin",
        "roles": ["AdapterModels.admin","AGManager.admin"]
    }]

    assert result["formatted_message"] == expected_message


def test_empty_users_list(mock_action_module, module_args, default_task_vars):
    """Test failure when users list is empty."""
    module_args["users"] = []  # Empty list
    result = run_module(mock_action_module, module_args, default_task_vars)

    assert result == {
        "failed": True,
        "msg": "The 'users' parameter must be provided and cannot be empty."
    }


def test_invalid_users_type(mock_action_module, module_args, default_task_vars):
    """Test failure when users is an invalid type (e.g., dict)."""
    module_args["users"] = {"username": "admin"}  # Invalid type
    result = run_module(mock_action_module, module_args, default_task_vars)

    assert result == {"failed": True, "msg": "The 'users' parameter must be a list or a string."}


def test_invalid_auth_accounts_type(mock_action_module, module_args, default_task_vars):
    """Test failure when auth_accounts is not a list."""
    module_args["auth_accounts"] = {"username": "admin"}  # Invalid type (dict instead of list)
    result = run_module(mock_action_module, module_args, default_task_vars)

    assert result == {
        "failed": True,
        "msg": "Both 'auth_accounts' and 'roles_response' must be lists."
    }


def test_invalid_roles_response_type(mock_action_module, module_args, default_task_vars):
    """Test failure when roles_response is not a list."""
    module_args["roles_response"] = "invalid_data"  # Invalid type (string instead of list)
    result = run_module(mock_action_module, module_args, default_task_vars)

    assert result == {
        "failed": True,
        "msg": "Both 'auth_accounts' and 'roles_response' must be lists."
    }
