# common - Define and check for common vars

This Ansible role manages the definition of common vars used by the rest of the collection. Your playbook is not required
to include this role as it is listed as a dependency of most roles.

## Role Variables

Only variables users are expected to be set are listed here.

| Variable Name                       | Description                        | Default Value      |
|-------------------------------------|------------------------------------|--------------------|
| `polaris_apps_project_name`         | The project name (folder name)     | `` (must be set)   |
| `polaris_apps_service_name`         | The service name (folder name)     | `` (must be set)   |
| `polaris_apps_service_install_name` | The install name (folder name)     | `` (must be set)   |
| `polaris_apps_service_port`         | Port number. May use role to set.  | `8080`             |


## Tasks

The role performs the following tasks:

1. **Define common variables**: Defines common variables that are used by other roles
2. **Check playbook input vars**: Check that calling playbook has set input variables correctly

## Dependencies

See variables above that your playbook must set.
