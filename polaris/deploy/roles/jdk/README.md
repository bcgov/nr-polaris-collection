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


## Tasks

The role performs the following tasks:

1. **Ensure Directory Structure Exists**: Creates `jdk_home` with appropriate permissions.
2. **Retrieve JDK Metadata**: Uses Adoptium API to get details of the requested JDK version.
3. **Download and Extract JDK**: Fetches and extracts the JDK package.
4. **Configure Certificates**: Downloads and imports certificates into the JDK keystore (`cacerts`).
5. **Apply Intention Patch**: Updates NR Broker with JDK configuration information.

## Dependencies

This role depends on values from the common role for default variable settings.

Additionally, before running this role, ensure that the `create_project_directories` role has been executed to set up necessary directories.

## Example Playbooks

Use this role to deploy an Adoptium OpenJDK package in one of three ways:

1. **Latest version of the default major version**
2. **Latest version of a specific major version**
3. **Pinned version of JDK**

The role fetches JDK release information and downloads packages from Adoptium API.

### Deploy the Latest Version of the Default Major Version

```yaml
---
- hosts: all
  roles:
    - name: jdk
      vars:
        proxy_env: '{{ env_vars }}'
```

### Deploy the Latest Version of a Specific Major Version

```yaml
---
- hosts: all
  roles:
    - name: jdk
      vars:
        jdk_major_version: '8'
        proxy_env: '{{ env_vars }}'
```

### Deploy a Specific Pinned Version

```yaml
---
- hosts: all
  roles:
    - name: jdk
      vars:
        jdk_pinned_release_name: 'jdk8u412-b08'
        proxy_env: '{{ env_vars }}'
```

To determine the available release names, refer to the Adoptium API:
[Adoptium API - Search Releases](https://api.adoptium.net/q/swagger-ui/#/Assets/searchReleases).
