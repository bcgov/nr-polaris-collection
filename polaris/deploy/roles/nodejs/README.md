# Node.js installation

Installs a specified version of Node.js, following Ministry conventions. Optionally, an arbitrary number of webapps may be installed.

This role observes a number of conventions:
* Node.js will be installed to `nodejs_install_dir`, which defaults to `pd_prop_service_install_directory`/nodejs;
* Logs are written to `pd_prop_service_logs`/, referenced by `nodejs_log_dir`;
* Webapps are installed to `pd_prop_service_install_directory`/webapps, referenced by `nodejs_webapp_dir`

*****

## Installation visualization

```
.
├─ <pd_prop_service_install_directory>/
|   ├─ <nodejs_install_dir>/
|   |   ├─ bin/
|   ├─ webapps/   # exists outside of the nodejs directory to allow easier upgrades of the container
└─ <pd_prop_service_logs>/
    ├─ nodejs.log
```

*****

## Role Variables

| variable                | default                             | description                                                                                            |
|-------------------------|-------------------------------------|--------------------------------------------------------------------------------------------------------|
| `nodejs_webapps`        | {}                                  |                                                                     |
| `nodejs_install_root`   | `pd_prop_service_install_directory` | The root that nodejs should be installed in to. By default, this will create a subfolder called nodejs |
| `nodejs_data_dir`       | `pd_prop_service_data`              |                                                                                                        |
| `nodejs_log_dir`        | `pd_prop_service_logs`              |                                                                                                        |
| `nodejs_version_number` | no default value                    |                                                                                                        |
| `nodejs_install_dir`    | `nodejs_install_root`/nodejs        |                                                                                                        |
| `nodejs_webapp_dir`     | `nodejs_install_root`/webapps       |                                                                                                        |

*****

## Example Playbook
```yml
---
- hosts: all
  become: yes
  vars:
    pd_prop_service_install_directory: "test"
    install_user: "wwwadm"
    apps_home: "/apps_home"
    apps_logs: "/apps_logs"
    apps_data: "/apps_data"
    s6_services: "/apps_ux/s6_services"
    pd_prop_project_name: "test_project"
    pd_prop_service_name: "test_service"
    nodejs_version_number: "latest-v22.x"
    app_js_name: "hello-world.js"
  roles:
    - create_project_directories
    - nodejs
```
