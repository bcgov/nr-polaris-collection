# Patch Intention Role

The Patch Intention role is responsible for generating and sending a PATCH request to the NR Broker. It takes input variables to customize the payload sent in the request.

## Requirements

This role requires Ansible collection "nr-polaris-collection" to be installed on the system where it will be executed.

## Role Variables

The following variables can be customized to modify the behavior of the role:

- `broker_url`: The URL for NR Broker where the PATCH request will be sent. (Default: "https://broker.io.nrs.gov.bc.ca")

- `action_token`: The action token for the PATCH request payload. (Default: The role uses the "ACTION_TOKEN_INSTALL" environment variable)

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
