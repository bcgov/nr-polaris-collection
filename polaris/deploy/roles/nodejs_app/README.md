# nodejs_app Node.js Application installation

Installs a Node.js application, following Ministry conventions.

## Role Variables

| Variable Name                   | Description                         | Default Value            |
|---------------------------------|-------------------------------------|--------------------------|
| `nodejs_app_service_entrypoint` | The path to the js file to run      | `app/dist/main.js`       |
| `nodejs_app_node_options`       | Options to pass to the node binary  | ``                       |

## Tasks

The role performs the following tasks:

* Copies files to the server to `nodejs_app_service_install_app_home`
* Creates files to start/stop service and writes environment variable files
* Ensure service is started

## Dependencies

This role's default values are dependant on the values in the common role.

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