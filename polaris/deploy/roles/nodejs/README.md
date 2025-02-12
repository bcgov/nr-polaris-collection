# nodejs - Node.js installation

This Ansible role installs a specified version of Node.js while following Ministry conventions. It ensures proper directory structure, version management, and integrity verification during installation.

If a specific version of Node.js is required, override nodejs_version_number in your playbook.

## Role Variables

| Variable Name           | Description                         | Default Value            |
|-------------------------|-------------------------------------|--------------------------|
| `nodejs_version_number` | The node version to install         | `latest-v22.x`           |
| `nodejs_install_user`     | The system user who will own the installation         | `{{ polaris_install_user }}` |
| `nodejs_install_dir`      | The directory where Node.js will be installed         | `"nodejs"` |
| `nodejs_bin_home`         | The base directory for binaries                      | `{{ polaris_apps_service_install_bin_home }}` |
| `nodejs_tmp_home`         | Temporary storage location for downloads             | `{{ polaris_apps_service_install_tmp_home }}` |
| `nodejs_mirror`           | The mirror URL for downloading Node.js               | `https://nodejs.org/download/release` |
| `nodejs_checksum_protocol` | The checksum validation protocol (e.g., `sha256`) | `"sha256"` |

## Dependencies

This role depends on values from the common role for default variable settings.

Additionally, before running this role, ensure that the `create_project_directories` role has been executed to set up necessary directories.

## Installation visualization

After installation, the Node.js files will be organized as follows:

```
.
├── <polaris_apps_service_install_home>/
│   ├── {{ polaris_bin_folder }}/{{ nodejs_install_dir }}/...
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
