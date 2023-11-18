# JDK

Installs a Java JDK with strong encryption enabled and default certificates added to cacerts.  The JDK directory is created in `jdk_install_root` and is named 'jdk' or using the value of `jdk_install_dir`.  For example,
```
/sw_ux/jdk
```

This role installs the appropriate distribution based on OS, platform, and Java version.
The state of this role is: **Preview**

## Role Variables

### Required

| variable name     | type    | default | description |
| ------------------|---------|---------|-------------|
| `jdk_install_root` | string | /sw_ux | The directory in which the JDK directory will be placed |


### Optional
| variable name     | type    | default | description |
| ------------------|---------|---------|-------------|
| `jdk_version` | string | 8 | JDK version - 7 or 8 |
| `jdk_install_dir` | string | jdk | The name of the JDK directory itself |
| `jdk_install_as` | string | wwwadm | The user account owning the JDK directory |
| `jdk_type` | string | oracle | Options include: oracle, openjdk |


### Example Playbook

```
- hosts: my-jdk-servers
  roles:
    - { role: jdk, jdk_install_root: '/apps_ux/myapp' } # export JAVA_HOME=/apps_ux/myapp/jdk
```
