# create_project_directories - Create directory structure on server

This Ansible role manages the creation of directories for a service. It ensures the required directory structure is in place, sets the current service version, and removes old service installation directories while retaining at least the three most recent versions.

## Role Variables

| Variable Name                     | Description                                | Default Value                           |
|-----------------------------------|--------------------------------------------|-----------------------------------------|
| `pd_install_user`                 | User to perform the directory operations   | `{{polaris_install_user}}`              |
| `pd_apps_project_home`            | Path to the project directory              | `{{polaris_apps_project_home}}`         |
| `pd_apps_service_home`            | Path to the service directory              | `{{polaris_apps_service_home}}`         |
| `pd_apps_service_current_home`    | Path to the current service directory      | `{{polaris_apps_service_current_home}}` |
| `pd_apps_service_install_home`    | Path to the installation service directory | `{{polaris_apps_service_install_home}}` |
| `pd_apps_service_logs_home`       | Base directory for logs                    | `{{polaris_apps_service_logs_home}}`    |
| `pd_apps_service_data_home`       | Base directory for application data        | `{{polaris_apps_service_data_home}}`    |
| `pd_remove_existing`              | If truthy wipe existing directories        | `no`                                    |

## Tasks

The role performs the following tasks:

1. **Debug Service Installation Directory**: Outputs the service installation directory for verification purposes.
2. **Create Project Directories**: Creates the necessary directory structure for the project and service.
3. **Set Current Version**: Creates a symbolic link named `current` pointing to the specified install version directory.
4. **Clean Up Old Service Installation Directories**: Deletes the oldest service installation directory if more than three exist.

## Dependencies

This role's default values are dependant on the values in the common role.

## Example Playbooks

```
roles:
  - role: create_project_directories
    vars:
      pd_remove_existing: yes
```
