# java_app - Java Application installation

This Ansible role automates the deployment of a Java application (specifically Spring Boot) by ensuring proper directory creation, downloading artifacts from GitHub Maven packages, copying configuration files, and managing the service lifecycle using the `service_control` role.

The role supports optional integration with Envconsul for injecting secrets from Vault into the application environment at startup.

## Role Variables

All variables are prefixed with `java_app_` to indicate they are specific to this role.

| Variable Name                         | Description                                                     | Default Value  |
|---------------------------------------|-----------------------------------------------------------------|-----------------|
| `java_app_artifact_url`               | URL to download the JAR artifact from GitHub Maven packages     | `""` (required) |
| `java_app_artifact_md5`               | MD5 checksum of the artifact for integrity verification         | `""` (required) |
| `java_app_artifact_name`              | Name of the artifact file                                       | `""` (required) |
| `java_app_artifact_download_dir`      | Directory where artifact will be downloaded                     | `/ansible/downloads/` |
| `java_app_install_user`               | User who will own the installation                              | `{{ polaris_install_user }}` |
| `java_app_service_user`               | User under which the application runs                           | `{{ polaris_service_user }}` |
| `java_app_service_install_home`       | Base installation directory for the application                 | `{{ polaris_apps_service_install_home }}` |
| `java_app_service_current_home`       | Directory of the currently active application version           | `{{ polaris_apps_service_current_home }}` |
| `java_app_service_install_app_home`   | Directory where the application JAR will be installed           | `{{ polaris_apps_service_install_app_home }}` |
| `java_app_service_data_home`          | Directory for application data storage                          | `{{ polaris_apps_service_data_home }}` |
| `java_app_service_log_home`           | Directory for application logs                                  | `{{ polaris_apps_service_logs_home }}` |
| `java_app_service_install_tmp_home`   | Temporary directory for installation processes                  | `{{ polaris_apps_service_install_tmp_home }}` |
| `java_app_service_port`               | Port on which the application runs                              | `{{ polaris_apps_service_port }}` |
| `java_app_jdk_install_dir`            | Directory name where JDK is installed                           | `jdk` |
| `java_app_jdk_home`                   | Path to the JDK installation directory                          | `{{ java_app_service_install_home }}/{{ polaris_bin_folder }}/{{ java_app_jdk_install_dir }}` |
| `java_app_properties_dir`             | Directory where application property files are stored           | `{{ java_app_service_install_app_home }}` |
| `java_app_properties_files`           | List of property files to copy to the server                    | `[]` |
| `java_app_jvm_options`                | JVM options for the application (e.g., heap size)               | `-Xms128m -Xmx512m` |
| `java_app_use_envconsul`              | Whether to use Envconsul for secret management                  | `true` |
| `java_app_envconsul_config_dir`       | Directory for Envconsul configuration files                     | `{{ java_app_service_install_home }}/envconsul.d` |
| `java_app_envconsul_upstreams`        | List of Vault paths for Envconsul to fetch secrets from         | `[]` |
| `java_app_env_dict`                   | Dictionary of environment variables to export                   | (optional) |

## Role Requirements

Before running this role, ensure that the following roles have been executed:

- `create_project_directories` - Creates the directory structure required by this role
- `jdk` - Installs and configures Java Development Kit
- `envconsul` (optional) - If using Envconsul for secret management, this role must be installed first

## Tasks

The role performs the following tasks:

1. **Ensure Prerequisite Role Execution**
   - Checks if `create_project_directories` was executed; fails otherwise.

2. **Stop the Running Application**
   - Stops the application before deploying new files to prevent conflicts.

3. **Create Required Directories**
   - Ensures the necessary directories exist for the application, logs, and data storage.

4. **Download Artifact from GitHub Maven packages**
   - Downloads the JAR artifact from the specified GitHub Maven package URL with MD5 checksum verification.

5. **Copy Artifact to Application Home**
   - Copies the downloaded JAR to the application installation directory as `app.jar`.

6. **Copy Properties Files**
   - Copies any specified property files (e.g., `application.properties`, `application.yml`) to the application directory.

7. **Deploy Startup and Environment Scripts**
   - Deploys `startup.sh` for launching the application.
   - Deploys `setenv.sh` for setting up environment variables and properties.

8. **Configure Envconsul (if enabled)**
   - Creates Envconsul configuration directory.
   - Deploys `envconsul.hcl` configuration if Vault upstreams are specified.

9. **Setup Service Handler**
   - Configures the service handler for managing the application lifecycle (systemd, s6, or script-based).

10. **Start the Service**
    - Starts the Java application using the configured service handler.

## Installation Visualization

```
.
├─ <java_app_service_install_home>/
│  ├─ bin/jdk/
│  │  ├─ bin/
│  │  └─ lib/
│  ├─ bin/envconsul/
│  │  └─ envconsul
│  ├─ envconsul.d/
│  │  └─ app.hcl
│  ├─ startup.sh
│  └─ setenv.sh
├─ <java_app_service_install_app_home>/
│  ├─ app.jar
│  ├─ application.properties (if provided)
│  └─ application.yml (if provided)
├─ <java_app_service_data_home>/
│  └─ data/
└─ <java_app_service_log_home>/
   └─ java.log
```

## Example Playbook - Basic Spring Boot Application

```yaml
---
- hosts: all
  become: yes
  vars:
    polaris_apps_project_name: "demo_project"
    polaris_apps_service_name: "demo_service"
    polaris_apps_service_install_name: "v1"
    java_app_artifact_url: "https://maven.pkg.github.com/bcgov/java-maven-pipeline-example/bcgov/example/java-maven-pipeline-example/1.0.1-main-SNAPSHOT/java-maven-pipeline-example-1.0.1-main-20250818.180118-27.jar"
    java_app_artifact_md5: "abcd1234ef5678901234567890abcdef"
    java_app_artifact_name: "app.jar"
    java_app_properties_files:
      - /path/to/application.properties
  roles:
    - create_project_directories
    - jdk
    - java_app
```

## Example Playbook - Spring Boot with Envconsul for Vault Secrets

```yaml
---
- hosts: all
  become: yes
  vars:
    polaris_apps_project_name: "secure_project"
    polaris_apps_service_name: "secure_service"
    polaris_apps_service_install_name: "v1"
    java_app_artifact_url: "https://maven.pkg.github.com/bcgov/java-app/bcgov/example/java-app/1.0.0/java-app-1.0.0.jar"
    java_app_artifact_md5: "abcd1234ef5678901234567890abcdef"
    java_app_artifact_name: "app.jar"
    java_app_use_envconsul: true
    java_app_envconsul_upstreams:
      - path: "secret/data/apps/myapp/db"
      - path: "secret/data/apps/myapp/api-keys"
    java_app_env_dict:
      SPRING_PROFILES_ACTIVE: "production"
      LOGGING_LEVEL_ROOT: "INFO"
    java_app_jvm_options: "-Xms256m -Xmx1024m"
  roles:
    - create_project_directories
    - jdk
    - envconsul
    - java_app
```

## Dependencies

This role depends on values from the common role for default variable settings.

Additionally, this role requires:
- **jdk** - For Java runtime environment
- **create_project_directories** - For directory structure setup
- **envconsul** (optional) - For Vault secret integration

## Notes

- The startup script conditionally includes a custom `setenv-custom.sh` script if present, allowing for additional environment variable setup.
- The application runs as a Spring Boot JAR by default with `java -jar app.jar`.
- Properties files are copied to the application directory and should be referenced in Spring Boot configuration.
- When using Envconsul, the startup script will wrap the Java process, allowing Envconsul to inject secrets from Vault as environment variables before the application starts.
- The service is managed using the `service_control` role, supporting systemd, s6, or script-based handlers depending on configuration.
