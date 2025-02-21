# create_project_directories - Manage Directory Structure for a Service

This Ansible role ensures the correct directory structure for a service is in place. It handles the creation of necessary directories, sets the current service version symlink, and removes outdated service installation directories while retaining the three most recent versions.

## Role Variables

All variables are prefixed with `pd_` to indicate they are specific to this role.

| Variable Name                     | Description                                | Default Value                           |
|-----------------------------------|--------------------------------------------|-----------------------------------------|
| `pd_install_user`                 | User to perform the directory operations   | `{{polaris_install_user}}`              |
| `pd_apps_project_home`            | Path to the project directory              | `{{polaris_apps_project_home}}`         |
| `pd_apps_service_home`            | Path to the service directory              | `{{polaris_apps_service_home}}`         |
| `pd_apps_service_current_home`    | Path to the "current" service symlink      | `{{polaris_apps_service_current_home}}` |
| `pd_apps_service_install_home`    | Path to the installation directory         | `{{polaris_apps_service_install_home}}` |
| `pd_remove_existing`              | If truthy wipe existing directories        | `no`                                    |

## Tasks

The role performs the following tasks:

1. **Debug Service Installation Directory**: Outputs the service installation directory for verification purposes.
2. **Create Required Directories**: Ensures the necessary project and service directories exist with the correct permissions.
3. **Set Current Service Version**: Creates or updates a symbolic link `current` pointing to the latest service installation directory.
4. **Clean Up Old Service Installation Directories**: Retains the three most recent installation directories by removing the oldest ones when necessary.

## Dependencies

This role depends on values from the common role for default variable settings.

## Example Playbooks

```
roles:
  - role: create_project_directories
    vars:
      pd_remove_existing: yes
```
