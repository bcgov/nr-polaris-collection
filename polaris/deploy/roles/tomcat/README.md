# tomcat - Tomcat installation

This Ansible role automates the installation and configuration of Apache Tomcat on Linux systems. It supports deploying multiple web applications, HTTPS configuration, logging, and JNDI resources.

## Features

- Installs Tomcat to a configurable directory.
- Separates data, logs, and application directories for easier management and upgrades.
- Supports HTTPS out of the box.
- Allows deployment of multiple web applications.
- Configures logging and JNDI resources.
- Integrates with s6 process supervision (optional).
- Does **not** install a JDK; expects one to be provided.

## Conventions

- **Install Directory:** `tomcat_install_dir` (default: `tomcat_install_root`/tomcat)
- **Data Directory:** `tomcat_data_dir` (default: `pd_service_data`/tomcat)
- **Logs Directory:** `tomcat_log_dir` (default: `pd_service_logs`)
- **Java Home:** `tomcat_java_home` (default: `cd_app_home`/jdk)
- **Webapps Directory:** `tomcat_webapp_dir` (default: `pd_service_install_directory`/webapps)
- **HTTPS:** Enabled by default (`tomcat_use_https`)
- **Shutdown Port:** Disabled by default (`tomcat_shutdown_port: -1`)
- **JDK:** Must be provided externally (e.g., via [jdk role](../jdk))
- **Default HTTPS Port:** 8001 (override with `tomcat_https_port`)

## Role Variables

All variables are prefixed with `tomcat_`. Key variables include:

| Variable | Default | Description |
|----------|---------|-------------|
| `tomcat_webapps` | `[]` | List of webapps to deploy ([see below](#webapps)) |
| `tomcat_jndi_resources` | `[]` | List of JNDI resources ([see below](#jndi-resources)) |
| `tomcat_install_root` | `{{ polaris_apps_service_install_home }}` | Root install directory |
| `tomcat_data_dir` | `{{ polaris_apps_service_data_home }}/tomcat` | Data directory |
| `tomcat_log_dir` | `{{ polaris_apps_service_logs_home }}` | Logs directory |
| `tomcat_use_https` | `yes` | Enable HTTPS |
| `tomcat_https_port` | `8001` | HTTPS port |
| `tomcat_keystore_file` | `{{ tomcat_install_root }}/.keys/key.jks` | Keystore file |
| `tomcat_major_version` | `10` | Tomcat major version |
| `tomcat_version_number` | | Tomcat semantic version (e.g., `9.0.100`). If not set, the latest available version for the specified `tomcat_major_version` is used. |
| `tomcat_java_home` | `{{ tomcat_install_root }}/bin/jdk` | Java home directory |
| `tomcat_install_user` | `{{ polaris_install_user }}` | Install user |
| ... | ... | ... |

See the full variable table in the original documentation for more options.

## Role Tasks

This role includes tasks to automate the full lifecycle of Tomcat installation and configuration:

- **Download and extract Tomcat:** Retrieves the specified Tomcat version and unpacks it to the target directory.
- **Directory setup:** Creates required directories for installation, data, logs, and webapps with appropriate permissions.
- **Configuration:** Templates and deploys configuration files (e.g., `server.xml`, `setenv.sh`) based on provided variables.
- **Webapp deployment:** Downloads and deploys web applications as defined in `tomcat_webapps`.
- **JNDI resources:** Configures JNDI resources in `context.xml` or as specified.
- **HTTPS setup:** Configures HTTPS connector and keystore if enabled.
- **Service integration:** Optionally sets up s6 supervision for Tomcat process management.
- **Permissions:** Ensures correct ownership and permissions for all files and directories.

All tasks are idempotent and can be customized via role variables.

## Dependencies

This role depends on values from the common role for default variable settings.

Additionally, before running this role, ensure that the `create_project_directories` role has been executed to set up necessary directories.

## Webapps

Deploy web applications by specifying a list of maps in `tomcat_webapps`. Each map should include:

| Key | Example | Description |
|-----|---------|-------------|
| `url` | `https://.../app.war` | Artifact URL |
| `md5` | `e73043...` | MD5 checksum |
| `context` | `int#app##1.0.0` | Tomcat context name |
| `clean` | `yes` | Remove existing deployment (default: yes) |

Webapps are extracted to the Tomcat webapps directory. Additional configuration is the responsibility of the playbook.

## JNDI Resources

Define JNDI resources in `tomcat_jndi_resources` as a list of maps:

| Key | Required | Example | Description |
|-----|----------|---------|-------------|
| `name` | yes | `jdbc/mydb` | Resource name |
| `url` | yes | | JDBC URL |
| `username` | yes | | DB username |
| `password` | yes | | DB password |
| `type` | no | `javax.sql.DataSource` | Resource type |
| `driver` | no | `oracle.jdbc.OracleDriver` | JDBC driver |
| ... | ... | ... | ... |

## Example Playbooks

Install the latest release for the default Tomcat major version:

```yaml
- hosts: all
  roles:
  - name: tomcat
```

Install the latest release for a specific major version:

```yaml
- hosts: all
  roles:
  - role: tomcat
    vars:
      tomcat_major_version: '9'
```

Install a specific (pinned) release for a given major version:

```yaml
- hosts: all
  roles:
  - role: tomcat
    vars:
      tomcat_major_version: '9'
      tomcat_version_number: '9.0.100'
```

---

For more details, see the full variable list and comments in the role defaults and documentation.
