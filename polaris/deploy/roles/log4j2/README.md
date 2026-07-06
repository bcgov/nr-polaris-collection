# log4j2 - Install a log4j2.xml configuration file from a template

Configures and deploys a log4j2.xml configuration file to an existing Tomcat container.

See: [tomcat](../tomcat/README.md)

## Role Variables

All variables are prefixed with `log4j2_` to indicate they are specific to this role.

| variable | required | default | description |
| -------- | -------- | ------- | ----------- |
| `log4j2_log_archive_filename_pattern` | no | `{{polaris_apps_service_name}}.%d.log.gz` | Log archive filename pattern |
| `log4j2_log_dir` | no | `{{polaris_apps_service_logs_home}}` | Root log directory |
| `log4j2_log_filename` | no | `{{polaris_apps_service_name}}.log`| Log filename |
| `log4j2_log_quartzdesk_enabled` | no | `False` | Enable quartzdesk logger; see [log4j2_quartzdesk](#log4j2_quartzdesk) |
| `log4j2_loggers` | no | `[]` | See [log4j2_loggers map](#log4j2_loggers-map) |
| `log4j2_root_log_level` | no | `INFO` | Root log level |

## `log4j2_loggers` map

| key | value (e.g.) | description |
| --- | ------------ | ----------- |
| `name` | `ca.bc.gov` | Where to download the WAR file |
| `level` | `INFO` | MD5 checksum of the file |

Using the `log4j2_loggers` property will allow you to configure an arbitrary number of log4j loggers for your application. Given the following `log4j2_loggers`:
```yml
log4j2_loggers:
  - name: 'ca.bc.gov.nrs.myapp'
    level: 'DEBUG'
```

The following snippet will be included in the <log4j:configuration> element of log4j2.xml:
```xml
<logger name="ca.bc.gov.nrs.myapp">
  <level value="DEBUG" />
</logger>
```

## `log4j2_quartzdesk`

When `log4j2_log_quartzdesk_enabled` is `True`, the following snippet will be included in the <log4j:configuration> element of log4j2.xml:
```xml
<!--
Appender that passes all received log events to the QuartzDesk JVM Agent for
processing. Log events that are not produced by Quartz scheduler threads are
silently ignored.
-->
<QuartzDeskJvmAgent name="QUARTZDESK_JVM_AGENT">
  <PatternLayout pattern="[%d{ISO8601}] %-5p [%t] [%C:%L] - %m%n"/>
  <filters>
    <ThresholdFilter level="info"/>
  </filters>
</QuartzDeskJvmAgent>
```
