# NR Polaris Ansible Collection

Ansible collection for deploying applications using [Polaris Pipelines](https://github.com/bcgov-nr/polaris-pipelines).

This collection provides roles for the deployment and configuration of application services on NRIDS servers.

## Requirements

This collection requires Ansible 2.12 or higher.

This collection was designed for Red Hat Enterprise Linux 9.

## Roles

- [common](polaris/deploy/roles/common/README.md) - Defines variables used by the rest of the collection
- [create_project_directories](polaris/deploy/roles/create_project_directories/README.md) - Creates the directory structure for a service
- [jdk](polaris/deploy/roles/jdk/README.md) - Installs and configures Adoptium OpenJDK
- [nodejs](polaris/deploy/roles/nodejs/README.md) - Installs and configures Node.js
- [nodejs_app](polaris/deploy/roles/nodejs_app/README.md) - Installs a Node.js application
- [patch_intention](polaris/deploy/roles/patch_intention/README.md) - Sends a patch request to NR Broker to update the catalog
- [port_manager](polaris/deploy/roles/port_manager/README.md) - Automates the assignment and management of service ports
- [self_signed_cert](polaris/deploy/roles/self_signed_cert/README.md) - Creates a self-signed certificate for the service
- [service_control](polaris/deploy/roles/service_control/README.md) - Automates starting, stopping, and restarting installed services
- [tomcat](polaris/deploy/roles/tomcat/README.md) - Automates the installation and configuration of Apache Tomcat
- [webade_connection_jar](polaris/deploy/roles/webade_connection_jar/README.md) - Creates and installs a WebADE connection JAR file
- [webapp](polaris/deploy/roles/webapp/README.md) - Configures and deploys a WAR file to Tomcat

## Plugins

No external plugins. There is an internal [s6 module](polaris/deploy/plugins/modules/s6_service.py) that the [service_control](polaris/deploy/roles/service_control/README.md) role uses.

## Quick Start

Start by reviewing [common](polaris/deploy/roles/common/README.md), as every role includes it. It defines many of the [defaults](polaris/deploy/roles/common/defaults/main.yml) that other roles use. If you want a value to be picked up globally, define one of the values from this role. If you want a value to be used only by a single role, define the role-specific variable.

Next, [create_project_directories](polaris/deploy/roles/create_project_directories/README.md) is used to create the directory structure for a service. Other roles require that this role be called first.

After this, playbooks call various roles to add binaries, application files, and configure the application as required.

## Related Products

* [NR Broker](https://github.com/bcgov/nr-broker)
* [NR Repository Composer](https://github.com/bcgov/nr-repository-composer)
* [Polaris Pipelines](https://github.com/bcgov-nr/polaris-pipelines)

## Development

Developing the roles requires having a machine available to target with Ansible. It is highly recommended to use Vagrant to create a local virtual machine using the provided Vagrantfile. The local VM can be provisioned from scratch in a couple of minutes.

In addition, application developers can use the Vagrant VM to test their playbooks. Most deployment issues can be resolved this way without needing to deploy to real servers.

### Required

* [Vagrant](https://developer.hashicorp.com/vagrant)
* [VirtualBox](https://www.virtualbox.org) (on macOS)

### Running the development box

This will set up the development virtual machine. It will take some time to download the image and complete the setup.

```
vagrant up
```

### Copy files to the development box

```
vagrant upload polaris
vagrant upload test polaris/deploy
```

### Use test playbooks

Connect to the virtual machine and run the playbook. You can then check the state of the virtual machine, re-upload files, and re-run as needed.

```
vagrant ssh
cd polaris/deploy
export ANSIBLE_LIBRARY=/home/vagrant/polaris/deploy/plugins
ansible-playbook nodejs.yml
/apps_ux/sample/service/artifact/bin/nodejs/bin/node -v
curl localhost:8080
```

### Run an application playbook locally - NodeJs

```
vagrant up
vagrant upload polaris
vagrant upload <application root>/playbooks polaris/deploy
vagrant upload overlay_nodejs polaris/deploy
vagrant ssh
mkdir -p polaris/app
cd polaris/app
oras pull ghcr.io/bcgov/nodejs-sample/package:v3.1.0
cd ../deploy
export ANSIBLE_LIBRARY=/home/vagrant/polaris/deploy/plugins
ansible-playbook -e env_vars=vagrant playbook.yaml
```

### Why no container?

We do not provide a container image for use with Podman or Docker because applications are installed into a stateful server. Containers are set up to run a single executable with no system services (like SSH) available. They also have a simplified file system security model.

In the end, we want to mimic the server and not simply run the application. The VM created by Vagrant operates like a server in ways a container cannot replicate.

# License

See: [LICENSE](./LICENSE)
