# jdk - JDK Installation and Configuration

This Ansible role automates the installation and configuration of Adoptium OpenJDK on a Linux system. It supports downloading and installing both the latest and specific versions, and configuring certificates.

## Role Variables

All variables are prefixed with `jdk_` to indicate they are specific to this role.

| Variable Name               | Description                                          | Default Value |
|-----------------------------|------------------------------------------------------|---------------|
| `jdk_install_root`          | Root directory for JDK installation                 | `{{ polaris_apps_service_install_bin_home }}` |
| `jdk_home`                  | Directory where JDK will be installed               | `{{ jdk_install_root }}/{{ jdk_install_dir }}` |
| `jdk_major_version`         | Major version of JDK to install                     | `21`          |
| `jdk_pinned_release_name`   | Specific JDK version to install                     | `""` (latest) |
| `jdk_install_dir`           | Directory name for JDK installation                 | `jdk`         |
| `jdk_install_as`            | User to perform the installation                    | `{{ polaris_install_user }}` |
| `jdk_type`                  | Type of JDK to install (`openjdk`)                  | `openjdk`     |
| `jdk_cacerts_file`          | Path to JDK keystore file                           | `{{ jdk_home }}/jre/lib/security/cacerts` |
| `jdk_keytool`               | Path to keytool binary                              | `{{ jdk_home }}/bin/keytool` |
| `jdk_cacerts_pass`          | Password for the JDK keystore                       | `{{ lookup('ansible.builtin.env', 'PODMAN_JDK_CACERTS_PASS') }}` |
| `jdk_certs`                 | List of certificates to import                      | See Below     |

### Default Certificate List

| Name                                      | URL |
|-------------------------------------------|-----|
| `IDIR_Infrastructure_Authority1.cer`     | `{{ artifactory_url }}/ext-binaries-local/certs/IDIR_Infrastructure_Authority1.cer` |
| `IDIR_Infrastructure_Authority2.cer`     | `{{ artifactory_url }}/ext-binaries-local/certs/IDIR_Infrastructure_Authority2.cer` |
| `IDIR_Infrastructure_Authority3.cer`     | `{{ artifactory_url }}/ext-binaries-local/certs/IDIR_Infrastructure_Authority3.cer` |
| `IDIR_Infrastructure_Authority4.cer`     | `{{ artifactory_url }}/ext-binaries-local/certs/IDIR_Infrastructure_Authority4.cer` |
| `wildcard.nrs.bcgov.cer`                 | `{{ artifactory_url }}/ext-binaries-local/certs/wildcard.nrs.bcgov.cer` |
| `lets-encrypt-x3-cross-signed.der`       | `{{ artifactory_url }}/ext-binaries-local/certs/lets-encrypt-x3-cross-signed.der` |


## Role Tasks

The role performs the following tasks:

1. **Ensure Directory Structure Exists**: Creates `jdk_home` with appropriate permissions.
2. **Retrieve JDK Metadata**: Uses Adoptium API to get details of the requested JDK version.
3. **Download and Extract JDK**: Fetches and extracts the JDK package.
4. **Configure Certificates**: Downloads and imports certificates into the JDK keystore (`cacerts`).
5. **Apply Intention Patch**: Updates NR Broker with JDK configuration information.

## Dependencies

This role depends on values from the common role for default variable settings.

Additionally, before running this role, ensure that the `create_project_directories` role has been executed to set up necessary directories.

## Deploy Adoptium OpenJDK

By default, this role deploys the latest Adoptium OpenJDK LTS release for the major version specified by the `jdk_major_version` variable (see role
defaults for the specific major version).

You can override which Adoptium JDK release gets deployed by providing the following variables in your playbook:

- Set `jdk_major_version` to deploy the latest release of a different major version (e.g., `8`, `11`, `17`, `21`).
- Set `jdk_pinned_release_name` to deploy a specific pinned Adoptium release (e.g., `jdk17u80-b01`).

This approach allows you to flexibly control which Adoptium JDK version is installed.

## Example Playbooks

Deploy the latest default Adoptium OpenJDK LTS release:

```yaml
---
- hosts: all
  roles:
    - name: jdk
```

Deploy the latest release for a specific major version:

```yaml
---
- hosts: all
  roles:
    - name: jdk
      vars:
        jdk_major_version: '8'
```

Deploy a specific (pinned) release:

```yaml
---
- hosts: all
  roles:
    - name: jdk
      vars:
        jdk_pinned_release_name: 'jdk8u412-b08'
```

To determine the available release names, refer to the Adoptium API:
[Adoptium API - Search Releases](https://api.adoptium.net/q/swagger-ui/#/Assets/searchReleases).
