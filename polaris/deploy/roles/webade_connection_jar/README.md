# webade-connection-jar

Creates and installs a WebADE connection JAR file.

The password should be entered via prompt in the playbook.

Installs a Java JDK with strong encryption enabled and default certificates added to cacerts.  The JDK directory is created in `jdk_install_root` and is named 'jdk' or using the value of `jdk_install_dir`.  For example: `/sw_ux/jdk`

The state of this role is: **Preview**


## Role Variables

All variables are prefixed with `webade_` to indicate they are specific to this role.

### Required

| variable name     | default | description |
| ------------------|---------|-------------|
| `webade_java_home` | none | The path to the JDK |
| `webade_install_dir` | none | The directory in which the connection JAR is installed |
| `webade_env` | none | A short name for the environment, such as int, test, or prod |
| `webade_jdbc_url` | none | The JDBC URL for the given environment |
| `webade_db_user` | none | The database username for the WebADE schema |
| `webade_db_pass` | none | The database password for the WebADE schame |


### Optional
| variable name     | default | description |
| ------------------|---------|-------------|
| `webade_build_dir` | /tmp/webade-connection-jar | Directory where the JAR is built |
| `webade_min_connections` | 0 | Minimum number of DB connections |
| `webade_max_connections` | 10 | Maximum number of DB connections |


### Example Usage
The role is included in another role's main tasks file.

```
# WebADE plugin connection JAR
# ----------------------------
- name: WebADE connection JAR
  include_role:
    name: webade-connection-jar
  vars:
    webade_java_home: "{{ wso2am_java_home }}"
    webade_install_dir: "{{ wso2am_install_dir }}/repository/components/lib"
    webade_env: "{{ wso2am_env }}"
    webade_jdbc_url: "{{ wso2am_webade_jdbc_url }}"
    webade_db_user: "{{ wso2am_webade_db_user }}"
    webade_db_pass: "{{ wso2am_webade_db_pass }}"
  become: yes
  become_user: "{{ wso2am_install_user }}"
```
The password is prompted in the playbook.
```
  vars_prompt:
    - name: wso2am_webade_db_pass
      prompt: "[ WebADE Connection ]: Enter Oracle DB password or Enter for none: "
```
