# port_manager - Automated port assignment

The `port_manager` role automates the assignment and management of service ports to ensure that applications run without conflicts. It creates a port management script, checks available ports, assigns one to the service, and cleans up temporary files after execution.

The assigned port can be accessed via `polaris_apps_service_port` for use in application configurations after calling this role.

## **Role Variables**

All variables are prefixed with `portmanager_` to indicate they are specific to this role.

These variables control the behavior of the port management process and can be overridden as needed:

| Variable Name                  | Description                                                | Default Value                                    |
|--------------------------------|------------------------------------------------------------|--------------------------------------------------|
| `portmanager_install_user`     | The user executing the port management tasks               | `{{ polaris_install_user }}`                     |
| `portmanager_app_dir`          | Directory where applications are installed                 | `{{ polaris_apps_home }}`                        |
| `portmanager_first_dir`        | Directory for the initial port assignment check            | `{{ polaris_apps_project_name }}/{{ polaris_apps_service_name }}` |
| `portmanager_script_name`      | Name of the port management script                        | `port_manager.pl`                                |
| `portmanager_assignments`      | Dictionary of assigned ports per host                      | `{}` (empty)                                     |
| `portmanager_debug`            | Whether to keep debugging artifacts (`true` or `false`)    | `false`                                          |
| `portmanager_service_home`     | Directory where assigned port details are stored           | `{{ polaris_apps_service_home }}`                |



## Tasks

1. **Ensure Prerequisite Role Execution**
   - The role checks if `create_project_directories` has been executed before proceeding.

2. **Generate the Port Management Script**
   - The script is created from a Jinja2 template (`{{ portmanager_script_name }}.j2`) and placed in `/tmp/` with executable permissions.

3. **Execute the Port Management Script**
   - The script is run to check for an available port.
   - If the script fails, execution stops to prevent incorrect port assignment.

4. **Assign and Register Ports**
   - The assigned port(s) are registered as facts for later use in the playbook.
   - The assigned port is stored under `polaris_apps_service_port`.

5. **Clean Up Port Management Scripts**
   - If debugging is disabled (`portmanager_debug: false`), the script is removed from `/tmp/`.

6. **Record Port in Service Home**
   - The assigned port is recorded in `portmanager_service_home`.


## Example Playbooks

```yaml
---
- hosts: all
  become: yes
  vars:
    portmanager_script_name: "port_manager"
  roles:
    - create_project_directories
    - port_manager
```
