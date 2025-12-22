# oci_app - Generic OCI Application Runner

This Ansible role automates the deployment of a generic application by ensuring proper directory creation, copying application files, and managing the service lifecycle using the `service_control` role.

This role is designed to be runtime-agnostic and can run any executable application (binaries, scripts, etc.) by configuring the `oci_app_service_command` variable. It integrates with the `jdk` and `nodejs` roles by providing pre-configured paths to runtimes installed by those roles.

## Role Variables

All variables are prefixed with `oci_app_` to indicate they are specific to this role.

| Variable Name                            | Description                                                  | Default Value  |
|------------------------------------------|--------------------------------------------------------------|----------------|
| `oci_app_service_copy_src`               | Source directory containing the application files            | `/ansible/downloads/app/` |
| `oci_app_install_user`                   | User who will own the installation                           | `{{ polaris_install_user }}` |
| `oci_app_service_user`                   | User under which the application runs                        | `{{ polaris_service_user }}` |
| `oci_app_service_install_home`           | Base installation directory for the application              | `{{ polaris_apps_service_install_home }}` |
| `oci_app_service_current_home`           | Directory of the currently active application version        | `{{ polaris_apps_service_current_home }}` |
| `oci_app_service_install_app_home`       | Directory where the application will be installed            | `{{ polaris_apps_service_install_app_home }}` |
| `oci_app_service_data_home`              | Directory for application data storage                       | `{{ polaris_apps_service_data_home }}` |
| `oci_app_service_log_home`               | Directory for application logs                               | `{{ polaris_apps_service_logs_home }}` |
| `oci_app_service_install_tmp_home`       | Temporary directory for installation processes               | `{{ polaris_apps_service_install_tmp_home }}` |
| `oci_app_service_port`                   | Port on which the application runs                           | `{{ polaris_apps_service_port }}` |
| `oci_app_runtime_install_dir`            | Directory name where the runtime is installed (e.g., `nodejs`, `jdk`) | `""` |
| `oci_app_runtime_home`                   | Path to the runtime installation directory                   | `{{ oci_app_service_install_home }}/{{ polaris_bin_folder }}/{{ oci_app_runtime_install_dir }}` |
| `oci_app_service_command`                | Command to execute the application                           | `./app` |
| `oci_app_service_working_dir`            | Working directory for the command                            | `{{ oci_app_service_install_app_home }}` |
| `oci_app_service_options`                | Additional command-line options for the application          | `""` |
| `oci_app_env_dict`                       | Dictionary of environment variables to set (optional)        | *undefined* |

## Tasks

The role performs the following tasks:

1. **Ensure Prerequisite Role Execution**
   - Checks if `create_project_directories` was executed; fails otherwise.

2. **Stop the Running Application**
   - Stops the application before copying new files to prevent conflicts.

3. **Create Required Directories**
   - Ensures the necessary directories exist for the application, logs, and data storage.

4. **Copy Application Files to the Server**
   - Archives and copies the application to the installation directory.

5. **Deploy Start and Environment Scripts**
   - Deploys `startup.sh` and `setenv.sh` for launching and configuring the application.

6. **Set Up the Service Handler**
   - Configures the service handler for managing the application lifecycle.

7. **Start the Service**
   - Uses `service_control` to start the application.

## Dependencies

This role depends on values from the common role for default variable settings.

Additionally, before running this role, ensure that the `create_project_directories` role has been executed to set up necessary directories.

## Installation Visualization

```
.
├─ <oci_app_service_install_home>/
|   ├─ startup.sh
|   ├─ setenv.sh
|   ├─ app/<Your application>
└─ <oci_app_service_data_home>/
    ├─ data
└─ <oci_app_service_log_home>/
    ├─ app.log
```

## Example Playbooks

### Running a Binary Application
```yml
---
- hosts: all
  become: yes
  vars:
    polaris_apps_project_name: "test_project"
    polaris_apps_service_name: "test_service"
    polaris_apps_service_install_name: "v1"
  roles:
    - create_project_directories
    - role: oci_app
      vars:
        oci_app_service_command: "./myapp"
```

### Running a Node.js Application
```yml
---
- hosts: all
  become: yes
  vars:
    polaris_apps_project_name: "test_project"
    polaris_apps_service_name: "test_service"
    polaris_apps_service_install_name: "v1"
  roles:
    - create_project_directories
    - nodejs
    - role: oci_app
      vars:
        oci_app_runtime_install_dir: "{{ nodejs_install_dir }}"
        oci_app_service_command: "{{ oci_app_runtime_home }}/bin/node"
        oci_app_service_options: "app/dist/main.js"
        oci_app_env_dict:
          NODE_ENV: "production"
```

### Running a Java Application
```yml
---
- hosts: all
  become: yes
  vars:
    polaris_apps_project_name: "test_project"
    polaris_apps_service_name: "test_service"
    polaris_apps_service_install_name: "v1"
  roles:
    - create_project_directories
    - jdk
    - role: oci_app
      vars:
        oci_app_runtime_install_dir: "{{ jdk_install_dir }}"
        oci_app_service_command: "{{ oci_app_runtime_home }}/bin/java"
        oci_app_service_options: "-jar app.jar"
        oci_app_env_dict:
          JAVA_OPTS: "-Xmx512m"
```

### With Custom Environment Variables
```yml
---
- hosts: all
  become: yes
  vars:
    polaris_apps_project_name: "test_project"
    polaris_apps_service_name: "test_service"
    polaris_apps_service_install_name: "v1"
  roles:
    - create_project_directories
    - role: oci_app
      vars:
        oci_app_service_command: "./app"
        oci_app_env_dict:
          DATABASE_URL: "postgres://localhost:5432/mydb"
          LOG_LEVEL: "info"
```
