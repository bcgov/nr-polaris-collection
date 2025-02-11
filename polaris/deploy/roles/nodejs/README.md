# nodejs - Node.js installation

Installs the specified version of Node.js, following Ministry conventions.

## Role Variables

| Variable Name           | Description                         | Default Value            |
|-------------------------|-------------------------------------|--------------------------|
| `nodejs_version_number` | The node version to install         | `latest-v22.x`           |

## Dependencies

This role's default values are dependant on the values in the common role.

## Installation visualization

```
.
├─ <polaris_apps_service_install_home>/
|  {{ polaris_bin_folder }}/{{ nodejs_install_dir }}/...
```

## Example Playbooks

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
```
