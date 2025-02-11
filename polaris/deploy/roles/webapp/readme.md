# webapp - Install a war file for Tomcat

Configures and deploys a WAR file to an existing Tomcat container

## Role Variables

| variable | required | default | description |
| -------- | -------- | ------- | ----------- |
| `webapp_war` | yes | {} | See [webapp_war map](#webapp-war-map) |
| `webapp_component` | no | `cd_component` | The component name that this webapp manifests |
| `webapp_tomcat_webapps_dir` | no | `pd_service_install_directory`/webapps | |
| `webapp_log_archive_filename_pattern` | no | `pd_service_name`.%d.log.gz | |
| `webapp_log_dir` | no | `apps_logs`/`pd_project_name`/`pd_service_name` | |
| `webapp_log_filename` | no | `pd_service_name`.log| |
| `webapp_log_provider` | no | log4j2 | |
| `webapp_root_log_level` | no | INFO | |
| `webapp_staging_dir` | no | `cd_app_home` | Directory to use to extract & configure the webapp prior to deployment |
| `webapp_user` | no | wwwadm | |
| `webapp_configure_log4j_enabled` | no | True | If true, overwrite any existing `WEB-INF/classes/log4j2.xml` with template |
| `webapp_configure_context_enabled` | no | True | If true, overwrite any existing `META-INF/context.xml` with template |

## `webapp_war` map

| key | value (e.g.) | description |
| --- | ------------ | ----------- |
| `url` | https://bwa.nrs.gov.bc.ca/int/artifactory/ext-binaries-local/npe/npe-e2edemo-war-0.0.1-193.war | Where to download the WAR file |
| `md5` | e73043700820aff427ea5f67868d9a3c | MD5 checksum of the file |
| `context` | int#npe-e2edemo-war##0.0.1 | Used to set the folder that the archive gets extracted to, exposing the web app at the specified context. See Tomcat's [context naming](https://tomcat.apache.org/tomcat-7.0-doc/config/context.html#Naming) documentation for more details |
| `clean` | yes | Optional, defaults to yes. Whether an existing deployment of the same context should be removed prior to deploying |
| `username` | | Optional, defaults to Artifactory user agent. Used only if the artifact is coming from an external source |
| `password` | | Optional, same as above |
| `jndi_resources` | | Optional, adds provided JNDI resources to the webapp's context.xml file. See below for more details |
| `loggers` | | Optional, adds logger configurations to the webapp's log4j configuration. See below for more details |

```yml
webapp_war:
  url: 'https://bwa.nrs.gov.bc.ca/int/artifactory/ext-binaries-local/APPS/my-app-0.0.1-193.war'
  md5: 'e73043700820aff427ea5f67868d9a3c'
  context: 'int#my-app'
  jndi_resources:
    - name: 'jdbc/webade_bootstrap'
      url: "{{ bootstrap_ds_url }}"
      username: "{{ bootstrap_username }}"
      password: "{{ bootstrap_password }}"
```

## `webapp_war.jndi_resources` map

| key | required | value (e.g.) | description |
| --- | -------- | ------------ | ----------- |
| `name` | yes | jdbc/webade_bootstrap | |
| `url` | yes | | This value should be a variable to allow deploy time injection |
| `username` | yes | | This value should be a variable to allow deploy time injection |
| `password` | yes | | This value **must** be a variable to allow deploy time injection |
| `validation_query` | no | - | |
| `type` | no | javax.sql.Datasource | |
| `driver` | no | oracle.jdbc.OracleDriver | Any driver specified here must have its appropriate JAR added to `tomcat_install_dir`/lib |
| `initial_size` | no | 3 | |
| `max_active` | no | 10 | |
| `max_idle` | no | 20 | |
| `max_wait` | no | -1 | |


## Logging and the `webapp_war.loggers` map

Using the `loggers` property will allow you to configure an arbitrary number of log4j loggers for your application. Given the following webapp_war:
```yml
webapp_war:
  url: 'https://bwa.nrs.gov.bc.ca/int/artifactory/ext-binaries-local/APPS/my-app-0.0.1-193.war'
  md5: 'e73043700820aff427ea5f67868d9a3c'
  context: 'int#my-app'
  loggers:
    - name: 'ca.bc.gov.nrs.myapp'
      level: 'DEBUG'
```

The following snippet will be included in the <log4j:configuration> element of log4j.xml:
```xml
<logger name="ca.bc.gov.nrs.myapp">
  <level value="DEBUG" />
</logger>
```

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
| `validationInterval` | no | 30000 | Only run validation at most at this frequency (in milliseconds). If a connection is due for validation, but has been validated previously within this interval, it will not be validated again |
| `testWhileIdle` | no | yes | |
| `test_on_borrow` | no | true | Whether objects will be validated before being borrowed from the pool |
| `removeAbandoned` | no | yes | |
| `removeAbandonedTimeout` | no | 60000 |


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
    - { role: jdk, jdk_install_root: "{{ pd_service_install_directory }}", jdk_version: "8" }
    - { role: self-signed-cert, ssc_dir: "{{ pd_service_install_directory }}/.keys", ssc_java_home: "{{ pd_service_install_directory }}/jdk", ssc_format: 'pkcs12' }
    - { role: tomcat, tomcat_version_number: '8.5.20', tomcat_webapps: "{{ webapps }}" }
```