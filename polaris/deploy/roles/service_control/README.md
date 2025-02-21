# service_control - Service Control

This Ansible role manages a service using either the **s6 service manager** or custom **start/stop scripts**. It supports starting, stopping, restarting, and setting up the service dynamically based on provided variables.

## Role Variables

All variables are prefixed with `service_control_` to indicate they are specific to this role.

The following variables can be customized in your playbook or inventory:

| Variable | Default | Description |
|----------|---------|-------------|
| `service_control_action` | **Required** | The action to perform (`start`, `stop`, `restart`, `setup`). |
| `service_control_handler` | `{{ polaris_control_handler }}` | The service handler type (`s6` or `script`). |
| `service_control_target` | `{{ polaris_apps_service_name }}` | The name of the service being controlled. |
| `service_control_service_user` | `{{ polaris_service_user }}` | User under which the service runs. |
| `service_control_install_user` | `{{ polaris_install_user }}` | User who installed the service. |
| `service_control_home` | `{{ polaris_apps_service_current_home }}` | Home directory of the service. |
| `service_control_service_s6_home` | `{{ polaris_apps_service_s6_home }}` | S6 home directory (for `s6` handler). |
| `service_control_service_script_start` | `{{ polaris_apps_service_current_home }}/startup.sh` | Start script (for `script` handler). |
| `service_control_service_script_stop` | `{{ polaris_apps_service_current_home }}/shutdown.sh` | Stop script (for `script` handler). |

## Tasks

This role performs the following tasks if the action is not `setup`:
- Starts, stops, or restarts the service based on `service_control_action`.
- Calls the appropriate handler (`s6` or `script`).

This role performs the following tasks if the action is `setup`:
- Preforms setup tasks based on the `service_control_handler` type by including the tasks.

## Handlers
- **s6 Service Management**
  - Starts, stops, and restarts services using `s6_service`.
- **Script-Based Service Management**
  - Executes `startup.sh` and `shutdown.sh` scripts to control the service.

## Example Playbooks

The following playbooks assume that the variables `polaris_apps_service_name` and `polaris_apps_project_name` are set. The variable `polaris_apps_service_current_home` will be set the correct location by the common role.

### Start the Service
```yaml
- hosts: all
  roles:
    - role: service_control
      vars:
        service_control_action: start
        service_control_handler: s6
```

### Stop the Service
```yaml
- hosts: all
  roles:
    - role: service_control
      vars:
        service_control_action: stop
        service_control_handler: script
```

### Restart the Service
```yaml
- hosts: all
  roles:
    - role: service_control
      vars:
        service_control_action: restart
        service_control_handler: s6
```

### Setup the Service
```yaml
- hosts: all
  roles:
    - role: service_control
      vars:
        service_control_action: setup
        service_control_handler: script
```

