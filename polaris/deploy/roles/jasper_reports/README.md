# jasper_reports - Deploy Jasper reports

This role deploys reports to JasperReports Server instances.

## Requirements

- Ansible 2.17 or higher
- Access to the JasperReports Server
- The `xmllint` utility for XML parsing

## Role Variables

All variables are prefixed with `jasper_` to indicate they are specific to this role.

The following variables can be set to customize the role's behavior:

- `jasper_server_instance`: The instance of the JasperReports Server. Must be either 'JCRS' or 'NRSRS'.
- `jasper_project_name`: The name of the Jasper project. Must NOT be in the list of invalid project names.
- `jasper_ds_0_url`: The URL of the primary datasource.
- `jasper_ds_0_user`: The username for the primary datasource.
- `jasper_ds_0_password`: The password for the primary datasource.
- `jasper_deployer_url`: The URL used for deploying reports to the JasperReports Server.
- `jasper_deployer_user`: The username for deploying reports to the JasperReports Server.
- `jasper_deployer_password`: The password for deploying reports to the JasperReports Server.
- `jasper_cookie_key`: The key for the JasperReports Server loadbalancing cookie.
- `jasper_pause_seconds`: The number of seconds to pause before requesting the import status from the Jasper server

## Example Playbooks

This role can be used to deploy reports to one or more servers.

### Deploy reports to a single server

Use the following playbook to deploy reports to a single server (node 1) in dev, test or prod:

```yaml
- hosts: localhost
  connection: local
  collections:
    - polaris.deploy
  vars:
    jasper_server_instance: "JCRS"
    jasper_project_name: "FNIRS"
    jasper_ds_0_url: "jdbc:oracle:thin:@//hostname:port/service_name"
    jasper_ds_0_user: "user"
    jasper_ds_0_password: "password"
    jasper_deployer_url: "https://jasper.example.com"
    jasper_deployer_user: "deployer"
    jasper_deployer_password: "password"
    # Increase the number of seconds to wait before requesting the import status.
    # Only used for large numbers of reports where the import can take longer than 5 seconds to complete.
    jasper_pause_seconds: 60

  tasks:
    - name: Deploy reports to a single server
      include_role:
        name: jasper_reports
```

### Deploy reports to multiple servers

Use the following playbook and commands to deploy reports to dev, test and prod. Note that the test and prod environments are loadbalanced (deploy to two nodes).

```yaml
- hosts: localhost
  connection: local
  collections:
    - polaris.deploy
  vars:
    jasper_server_instance: "JCRS"
    jasper_project_name: "FNIRS"
    jasper_ds_0_url: "jdbc:oracle:thin:@//hostname:port/service_name"
    jasper_ds_0_user: "user"
    jasper_ds_0_password: "password"
    jasper_deployer_url: "https://jasper.example.com"
    jasper_deployer_user: "deployer"
    jasper_deployer_password: "password"

  tasks:
    - name: Create packages
      include_role:
        name: jasper_reports
      tags: create_packages

    - name: Deploy to node 1
      when: jasper_env in ["dev", "test", "prod"]
      include_role:
        name: jasper_reports
      tags: deploy_packages

    - name: Deploy to node 2
      when: jasper_env in ["test", "prod"]
      include_role:
        name: jasper_reports
      vars:
        jasper_route_id: ".2"
      tags: deploy_packages

    - name: Delete staging directory
      include_role:
        name: jasper_reports
      tags: delete_staging_dir
```

#### Commands

Create a package for a given environment:

```
ansible-playbook app/playbooks/jasper.yaml --tags create_packages
```

Deploy a package to the dev environment:

```
ansible-playbook app/playbooks/jasper.yaml --extra-vars "jasper_env=dev" --tags deploy_packages
```

Deploy a package to the dev and test environments:

```
ansible-playbook app/playbooks/jasper.yaml --extra-vars "jasper_env=test" --tags deploy_packages
```

Deploy a package to the dev, test and prod environments:

```
ansible-playbook app/playbooks/jasper.yaml --extra-vars "jasper_env=prod" --tags deploy_packages
```

Clean up by deleting the staging directory:

```
ansible-playbook app/playbooks/jasper.yaml --tags delete_staging_dir
```
