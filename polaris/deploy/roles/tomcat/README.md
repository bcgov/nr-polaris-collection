# Tomcat

Installs a specified version of Tomcat, following Ministry conventions. Optionally, an arbitrary number of webapps may be installed.

This role observes a number of conventions:
* Tomcat will be installed to `tomcat_install_dir`, which defaults to `cd_app_install`/tomcat;
* The tomcat/temp and tomcat/work folders are moved to `cd_app_data`/tomcat/*, referenced by `tomcat_data_dir`;
* Logs are written to `cd_app_logs`/, referenced by `tomcat_log_dir`;
* Java is assumed to be located in `cd_app_home`/jdk, referenced by `tomcat_java_home`
* HTTPS is enabled, referenced by `tomcat_use_https`
* Shutdown port is disabled by default (set to -1), referenced by `tomcat_shutdown_port`
* A JDK will not be installed as part of this role, it must be provided (i.e. by using the [jdk role](../jdk)).
* Webapps are installed to `cd_app_install`/webapps, referenced by `tomcat_webapp_dir`
* A default port of 8001 is applied, but it is **strongly** recommended that this be provided at deploy time by setting a variable of `tomcat_https_port`

*****

## Installation visualization

```
.
├─ <cd_app_install>/
|   ├─ <tomcat_install_dir>/
|   |   ├─ bin/
|   |   |   ├─ catalina.sh
|   |   |   ├─ setenv.sh
|   |   |   ├─ startup.sh
|   |   |   └─ shutdown.sh
|   |   └─ conf/
|   |       ├─ context.xml
|   |       ├─ server.xml
|   |       └─ logging.properties
|   ├─ webapps/   # exists outside of the tomcat directory to allow easier upgrades of the container
|   └─ jdk/       # this folder is assumbed to exist by convention, but it will not be created by the role. Override it by setting tomcat_java_home
├─ <cd_app_data>/
|   └─ <tomcat_data_dir>/
|       ├─ temp/
|       └─ work/
└─ <cd_app_logs>/
    ├─ localhost.access.log
    └─ catalina.out
```

*****

## Role Variables

| variable | default | description |
| -------- | ------- | ----------- |
| `tomcat_webapps` | {} | See [Webapps map](#webapps-map) |
| `tomcat_jndi_resources` | [] | See [JNDI resources](#jndi-resources) |
| `tomcat_install_root` | `cd_app_install` | The root that tomcat should be installed in to. By default, this will create a subfolder called Tomcat |
| `tomcat_data_dir` | `cd_app_data` | |
| `tomcat_log_dir` | `cd_app_logs` | |
| `tomcat_service_dir` | `cd_app_service` |  required if using s6 |
| `tomcat_use_https` | yes | |
| `tomcat_https_port` | 8001 | required if `tomcat_use_https` is true |
| `tomcat_keystore_file` | `tomcat_install_root`/.keys/key.jks | This default uses knowledge of the [self-signed certificate](../ssc) role |
| `tomcat_version_number` | 8.5.20 | See [role vars](vars/main.yml) for a list of supported versions |
| `tomcat_java_home` | `tomcat_install_root`/jdk | |
| `tomcat_install_dir` | `tomcat_install_root`/tomcat | |
| `tomcat_webapp_dir` | `tomcat_install_root`/webapps | |
| `tomcat_configure_logging_properties` | yes | |
| `tomcat_log_level` | INFO | |
| `tomcat_catalina_log_level` | `tomcat_log_level` | |
| `tomcat_localhost_log_level` | `tomcat_log_level` | |
| `tomcat_manager_log_level` | `tomcat_log_level` | |
| `tomcat_host_manager_log_level` | `tomcat_log_level` | |
| `tomcat_compression` | 'off' | Set to 'on' to enable compression |
| `tomcat_compressionMinSize` | 1024 | If compression is set to 'on' then this attribute may be used to specify the minimum amount of data (bytes) before the output is compressed |
| `tomcat_noCompressionUserAgents` | gozilla, traviata | The value is a regular expression (using java.util.regex) matching the user-agent header of HTTP clients for which compression should not be used, because these clients, although they do advertise support for the feature, have a broken implementation. |
| `tomcat_compressibleMimeType` | text/html,text/xml,text/plain,text/css,text/javascript,application/javascript,application/json,application/xml | The value is a comma separated list of MIME types for which HTTP compression may be used. |
| `tomcat_env_dict` | {} | Dictionary of values to output as environment variables in setenv.sh for tomcat applications to use. |

*****

## `tomcat_webapps` map
This role can deploy an arbitrary number of webapps to the Tomcat container, by accepting an optional list of webapps via the `tomcat_webapps` property. If provided, each listen item must contain a map with the following structure:

| key | value (e.g.) | description |
| --- | ------------ | ----------- |
| `url` | https://bwa.nrs.gov.bc.ca/int/artifactory/ext-binaries-local/npe/npe-e2edemo-war-0.0.1-193.war | Where to download the artifact containing the web app |
| `md5` | e73043700820aff427ea5f67868d9a3c | MD5 checksum of the file |
| `context` | int#npe-e2edemo-war##0.0.1 | Used to set the folder that the archive gets extracted to, exposing the web app at the specified context. See Tomcat's [context naming](https://tomcat.apache.org/tomcat-7.0-doc/config/context.html#Naming) documentation for more details |
| `clean` | yes | Optional, defaults to yes. Whether an existing deployment of the same context should be removed prior to deploying |

**Note**: Webapps will be extracted to the Tomcat webapps directory, but it is up to the calling playbook to perform any necessary configuration.

*****

## JNDI Resources
The role can accept an optional list of JNDI resource maps that will create resource entries in the container's server.xml file.

| key | required | value (e.g.) | description |
| --- | -------- | ------------ | ----------- |
| `name` | yes | jdbc/webade_bootstrap | |
| `url` | yes | | |
| `username` | yes | | |
| `password` | yes | | |
| `validation_query` | no | - | |
| `type` | no | javax.sql.Datasource | |
| `driver` | no | oracle.jdbc.OracleDriver | Any driver specified here must have its appropriate JAR added to `tomcat_install_dir`/lib |
| `initial_size` | no | 3 | |
| `max_active` | no | 10 | |
| `max_idle` | no | 20 | |
| `max_wait` | no | -1 | |

*****

## Example Playbook
```yml
---
- hosts: npe-e2edemo-war-servers
  vars:
    project:              NPE
    component:            npe-e2edemo-war
    artifact:             "{{ modules['npe-e2edemo-war'].artifacts['npe-e2edemo-war.war'] }}"
    target_environment:   "{{ target_environment | default('integration') }}"
    webapps:
      - { url: "{{ artifact.uri }}", md5: "{{ artifact.md5 }}", context: "int#e2edemo##{{ artifact.version }}" }
  roles:
    - cd-prepare
    - { role: jdk, jdk_install_root: "{{ cd_app_install }}", jdk_version: "8" }
    - { role: self-signed-cert, ssc_dir: "{{ cd_app_install }}/.keys", ssc_java_home: "{{ cd_app_install }}/jdk", ssc_format: 'pkcs12' }
    - { role: tomcat, tomcat_version_number: '8.5.20', tomcat_webapps: "{{ webapps }}" }
```
