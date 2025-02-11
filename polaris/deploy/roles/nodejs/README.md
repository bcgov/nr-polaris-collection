# nodejs - Node.js installation

Installs the specified version of Node.js, following Ministry conventions.

## Role Variables

| variable                | default                             | description                                                                                            |
|-------------------------|-------------------------------------|--------------------------------------------------------------------------------------------------------|
| `nodejs_webapps`        | {}                                  |                                                                     |
| `nodejs_install_root`   | `pd_service_install_directory` | The root that nodejs should be installed in to. By default, this will create a subfolder called nodejs |
| `nodejs_data_dir`       | `pd_service_data`              |                                                                                                        |
| `nodejs_log_dir`        | `pd_service_logs`              |                                                                                                        |
| `nodejs_version_number` | no default value                    |                                                                                                        |
| `nodejs_install_dir`    | `nodejs_install_root`/nodejs        |                                                                                                        |
| `nodejs_webapp_dir`     | `nodejs_install_root`/webapps       |                                                                                                        |
## Dependencies

This role's default values are dependant on the values in the common role.

## Installation visualization

```
├─ /{{ apps_home }}/{{ pd_project_name }}/{{ pd_service_name }}/
├─  ├─ <pd_service_install_directory>/
|   |   ├─ {{ polaris_bin_folder }}/{{ nodejs_install_dir }}/...
```

## Example Playbooks

```yml
---
- hosts: all
  become: yes
  vars:
    pd_service_install_directory: "test"
    install_user: "wwwadm"
    apps_home: "/apps_home"
    apps_logs: "/apps_logs"
    apps_data: "/apps_data"
    s6_services: "/apps_ux/s6_services"
    pd_project_name: "test_project"
    pd_service_name: "test_service"
    nodejs_version_number: "latest-v22.x"
    app_js_name: "hello-world.js"
  roles:
    - create_project_directories
    - nodejs
```
