# cd-prepare

This role is meant to ensure the creation of application directories as dictated by the Continuous Delivery pipeline. **This role has a tight integration with Jenkins**, and acts based on variables that are provided by a Jenkins deployment.

In addition to the default [Jenkins deployment variables](../../docs/JENKINSPLAYBOOK.md), this role will set `cd_app_service`. If the target host is [S6 enabled](../../docs/CONVENTIONS.md), then an S6 service directory will be created for the application. If not, it will instead create a hidden service directory inside the installation folder.
The state of this role is: **Stable**

## Required variables

| variable | example |
| -------- | ------- |
| `cd_app_container` | /apps_ux/NPE |
| `cd_app_home` | /apps/ux/NPE/npe-e2edemo-war |
| `cd_app_install` | /apps/ux/NPE/npe-e2edemo-war/1.0.1 |
| `cd_app_data` | /apps_data/npe-e2edemo-war |
| `cd_app_logs` | /apps_data/logs/npe-e2edemo-war |
| `cd_project` | NPE |
| `cd_component` | npe-e2edemo-war |
| `cd_build_number` | 12 |
| `s6_services` | /apps_ux/s6_services |

**Note**: `s6_services` is only required if s6_enabled is true on the target host. 

Example Playbook
----------------
```yaml
- hosts: my-target-servers
  roles:
    - cd-prepare 
    - { role: my-cool-role, mcr_home: "{{ cd_app_home }}" } # this directory is guaranteed to exist
```