# tomcat_context - Install a tomcat context.xml from a template

Configures and deploys a tomcat context.xml file to an existing Tomcat container.

See: [tomcat](../tomcat/README.md)

## Role Variables

All variables are prefixed with `tomcat_context` to indicate they are specific to this role.

| variable | required | default | description |
| -------- | -------- | ------- | ----------- |
| `tomcat_context_allow_casual_multipart_parsing` | no | `false` | Set allowCasualMultipartParsing |
| `tomcat_context.jndi_resources` | no | `{{polaris_apps_service_name}}` | The component name that this webapp manifests |

## `tomcat_context.jndi_resources` map
```yml
tomcat_context:
  jndi_resources:
    - name: 'jdbc/webade_bootstrap'
      url: "{{ bootstrap_ds_url }}"
      username: "{{ bootstrap_username }}"
      password: "{{ bootstrap_password }}"
```


## JNDI Resources
The role can accept an optional list of JNDI resource maps that will create resource entries in the container's server.xml file.

| key | required | value (e.g.) | description |
| --- | -------- | ------------ | ----------- |
| `name` | yes | `jdbc/webade_bootstrap` | |
| `url` | yes | | This value should be a variable to allow deploy time injection |
| `username` | yes | | This value should be a variable to allow deploy time injection |
| `password` | yes | | This value should be a variable to allow deploy time injection |
| `factory` | no | `org.apache.tomcat.jdbc.pool.DataSourceFactory` | |
| `type` | no | `javax.sql.Datasource` | |
| `driver` | no | `oracle.jdbc.OracleDriver` | Any driver specified here must have its appropriate JAR added to `tomcat_install_dir`/lib |
| `max_active` | no | `10` | |
| `max_idle` | no | `10` | |
| `min_idle` | no | `1` | |
| `initial_size` | no | `3` | |
| `max_wait` | no | `-1` | |
| `test_on_borrow` | no | `true` | Whether objects will be validated before being borrowed from the pool |
| `test_while_idle` | no | `yes` | |
| `validationQuery` | no | `SELECT sysdate from dual` | |
| `timeBetweenEvictionRunsMillis` | no | `5000` | |
| `removeAbandoned` | no | `yes` | |
| `removeAbandonedTimeout` | no | `60000` |
| `underlying_connection` | no | `false` |
| `initSQL` | no | `alter session set nls_numeric_characters = '.,'` | |

