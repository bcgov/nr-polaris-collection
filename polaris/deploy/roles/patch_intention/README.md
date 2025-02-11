# patch_intention - Send intention patch to NR Broker

This Ansible role is responsible for generating and sending a PATCH request to the NR Broker. It takes input variables to customize the payload sent in the request.

## Role Variables

The following variables can be customized to modify the behavior of the role:

- `broker_url`: The URL for NR Broker where the PATCH request will be sent. (Default: "https://broker.io.nrs.gov.bc.ca")
- `action_token`: The action token for the PATCH request payload. (Default: The role uses the "ACTION_TOKEN_INSTALL" environment variable)
- `_jdk_type`: The jdk type. (Default: empty string)
- `_jdk_major_version`: The major version of the jdk. (Default: empty string)
- `_jdk_url`: The url used to download the jdk. (Default: empty string)
- `_jdk_release_name`: The name of the jdk release. (Default: empty string)
- `_log_dir`: The base path to logs. (Default: empty string)
- `_log_level`: The log level. (Default: empty string)
- `_log_provider`: The component providing the logs (log4j2). (Default: empty string)
- `_log_type`: The log type (tomcat). (Default: empty string)
- `_tomcat_version`: The tomcat version for the PATCH request payload. (Default: empty string)
- `_tomcat_port`: The tomcat port for the PATCH request payload. (Default: empty string)

## Dependencies

This role does not have any dependencies.

## Example Playbook

Here's an example playbook that uses the `patch_intention` role:

```yaml
- hosts: localhost
  gather_facts: no
  roles:
    - role: patch_intention
      vars:
        _tomcat_version: "9.0.89"
        _tomcat_port: "8055"
