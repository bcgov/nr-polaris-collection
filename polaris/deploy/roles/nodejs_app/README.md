# nodejs_app - Node.js Application installation

This Ansible role automates the deployment of a Node.js application by ensuring proper directory creation, copying application files, and managing the service lifecycle using the `service_control` role.

If the application needs a different entrypoint, update nodejs_app_service_entrypoint. If the application needs specific runtime options, update nodejs_app_node_options.

## Role Variables

All variables are prefixed with `nodejs_app_` to indicate they are specific to this role.

| Variable Name                            | Description                                                  | Default Value  |
|------------------------------------------|--------------------------------------------------------------|---------------|
| `nodejs_app_service_copy_src`            | Source directory containing the application files            | `/ansible/downloads/app/` |
| `nodejs_app_install_user`                | User who will own the installation                           | `{{ polaris_install_user }}` |
| `nodejs_app_service_user`                | User under which the application runs                        | `{{ polaris_service_user }}` |
| `nodejs_app_service_install_home`        | Base installation directory for the application              | `{{ polaris_apps_service_install_home }}` |
| `nodejs_app_service_current_home`        | Directory of the currently active application version        | `{{ polaris_apps_service_current_home }}` |
| `nodejs_app_service_install_app_home`    | Directory where the application will be installed            | `{{ polaris_apps_service_install_app_home }}` |
| `nodejs_app_service_data_home`           | Directory for application data storage                       | `{{ polaris_apps_service_data_home }}` |
| `nodejs_app_service_log_home`            | Directory for application logs                               | `{{ polaris_apps_service_logs_home }}` |
| `nodejs_app_service_install_tmp_home`    | Temporary directory for installation processes               | `{{ polaris_apps_service_install_tmp_home }}` |
| `nodejs_app_service_port`                | Port on which the application runs                           | `{{ polaris_apps_service_port }}` |
| `nodejs_app_service_entrypoint`          | Entry point script for starting the application              | `app/dist/main.js` |
| `nodejs_app_node_install_dir`            | Directory name where Node.js is installed                    | `nodejs` |
| `nodejs_app_node_home`                   | Path to the Node.js installation directory                   | `{{ nodejs_app_service_install_home }}/{{ polaris_bin_folder }}/{{ nodejs_app_node_install_dir }}` |
| `nodejs_app_node_options`                | Additional Node.js runtime options                           | `""` |
| `nodejs_app_control_handler`             | The service handler used for managing the application        | `{{ polaris_control_handler }}` |


## Tasks

The role performs the following tasks:

1. **Ensure Prerequisite Role Execution**
   - Checks if `create_project_directories` was executed; fails otherwise.

2. **Stop the Running Application**
   - Stops the application before copying new files to prevent conflicts.

3. **Set Up the Service Handler**
   - Configures the service handler for managing the application lifecycle.

4. **Create Required Directories**
   - Ensures the necessary directories exist for the application, logs, and data storage.

5. **Copy Application Files to the Server**
   - Copies the application to the installation directory.

6. **Deploy Start and Environment Scripts**
   - Deploys `start.sh` and `setenv.sh` for launching and configuring the application.

7. **Start the Service**
   - Uses `service_control` to start the Node.js application.

## Dependencies

This role depends on values from the common role for default variable settings.

Additionally, before running this role, ensure that the `create_project_directories` role has been executed to set up necessary directories.

## Installation visualization

```
.
├─ <nodejs_app_service_install_home>/
|   ├─ bin/<nodejs_install_dir>/
|   |   ├─ bin/
|   ├─ app/<Your application>
└─ <nodejs_app_service_data_home>/
    ├─ data
└─ <nodejs_app_service_log_home>/
    ├─ nodejs.log
```

## Example Playbook
```yml
---
- hosts: all
  become: yes
  vars:
    polaris_apps_project_name: "test_project"
    polaris_apps_service_name: "test_service"
    polaris_apps_service_install_name: "v10"
  roles:
    - create_project_directories
    - nodejs
    - nodejs_app
```