# jdk: JDK Installation and Configuration

This Ansible role automates the installation and configuration of Adoptium OpenJDK on a Linux system. It supports downloading and installing both latest
and specific versions, configuring certificates and managing the JCE policy files.

## Role Variables

TBD

## Tasks

The role performs the following tasks:

1. **Create JDK Home Directory:** Creates the directory specified by `jdk_home` with the appropriate permissions.
2. **Fetch Asset Information:** Retrieves metadata for the specified JDK version using the Adoptium API.
3. **Download and Extract JDK:** Downloads the JDK package and extracts it to the specified location.
4. **Manage Certificates:** Downloads and imports certificates into the JDK's cacerts file.
5. **Configure JCE:** Downloads and installs the JCE policy files (for JDK 8).
6. **Patch Intention:** Patches the intention with the JDK version.

## Dependencies

This role's default values are dependant on the values in the common role.

## Example Playbooks

Use this role to deploy an Adoptium OpenJDK package in one of three ways: (1) the latest version of the default major version, (2) the latest
version of a given major version or (3) a specific pinned version. The role uses the Adoptium API to get release information and download packages.

### Deploy latest version of the default major version

To deploy the latest version of the default major version, simply call the role:

```yaml
---
- hosts: all
  roles:
    - name: jdk
      vars:
        proxy_env: '{{ env_vars }}'
```

### Deploy latest version of a given major version

To deploy the latest version of a given major version, call the role with the following variables:

```yaml
---
- hosts: all
  roles:
    - name: jdk
      vars:
        jdk_major_version: '8'
        proxy_env: '{{ env_vars }}'
```

### Deploy a specific pinned version

To deploy a specific pinned version, call the role with the following variables:

```yaml
---
- hosts: all
  roles:
    - name: jdk
      vars:
        jdk_pinned_release_name: 'jdk8u412-b08'
        proxy_env: "{{ env_vars }}"
```

Use the Adoptium API to determine the release name: https://api.adoptium.net/q/swagger-ui/#/Assets/searchReleases.
