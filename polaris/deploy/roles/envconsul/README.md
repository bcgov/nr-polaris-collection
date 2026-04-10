# envconsul - Envconsul Installation

This Ansible role installs a specified version of Envconsul, following Ministry conventions. It ensures proper directory structure, version management, and integrity verification during installation.

If a specific version of Envconsul is required, override `envconsul_version_number` in your playbook.

## Role Variables

| Variable Name              | Description                                 | Default Value            |
|----------------------------|---------------------------------------------|--------------------------|
| `envconsul_version_number` | The Envconsul version to install            | `0.13.4`                 |
| `envconsul_install_user`   | The system user who will own the installation | `{{ polaris_install_user }}` |
| `envconsul_install_dir`    | The directory where Envconsul will be installed | `envconsul`           |
| `envconsul_bin_home`       | The base directory for binaries             | `{{ polaris_apps_service_install_bin_home }}` |
| `envconsul_tmp_home`       | Temporary storage location for downloads    | `{{ polaris_apps_service_install_tmp_home }}` |
| `envconsul_mirror`         | The mirror URL for downloading Envconsul    | `https://releases.hashicorp.com/envconsul` |
| `envconsul_checksum_protocol` | The checksum validation protocol         | `sha256`                 |
| `envconsul_os`             | OS type (linux, etc.)                       | `linux`                  |
| `envconsul_arch`           | Architecture (amd64, etc.)                  | `amd64`                  |

## Dependencies

This role depends on values from the common role for default variable settings.

Before running this role, ensure that the `create_project_directories` role has been executed to set up necessary directories.

## Example Playbook

```yaml
- hosts: all
  become: yes
  roles:
    - create_project_directories
    - envconsul