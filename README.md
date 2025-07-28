# NR Polaris Ansible Collection

Ansible collection for deploying applications using [Polaris Pipelines](https://github.com/bcgov-nr/polaris-pipelines).

The collection provides roles for the deployment and configuration of application services on NRIDS servers.

## Requirements

This collection requires Ansible 2.12 or higher.

The collection was designed for Red Hat Enterprise Linux 9.

## Roles

- [common](polaris/deploy/roles/common/README.md) - Defines vars used by the rest of the collection
- [create_project_directories](polaris/deploy/roles/create_project_directories/README.md) - Creates the directory structure for a service
- [jdk](polaris/deploy/roles/jdk/README.md) - Installs and configures Adoptium OpenJDK
- [nodejs](polaris/deploy/roles/nodejs/README.md) - Installs and configures Node.js
- [nodejs_app](polaris/deploy/roles/nodejs_app/README.md) - Installs Node.js application
- [patch_intention](polaris/deploy/roles/patch_intention/README.md) - Send patch request to NR Broker to update catalog
- [port_manager](polaris/deploy/roles/port_manager/README.md) - Automates the assignment and management of service ports
- [self_signed_cert](polaris/deploy/roles/self_signed_cert/README.md) - Creates a self-signed certificate for the service
- [service_control](polaris/deploy/roles/service_control/README.md) - Automates start, stop and restart of installed services
- [tomcat](polaris/deploy/roles/tomcat/README.md) - Automates the installation and configuration of Apache Tomcat
- [webade_connection_jar](polaris/deploy/roles/webade_connection_jar/README.md) - Creates and installs a WebADE connection JAR file
- [webapp](polaris/deploy/roles/webapp/README.md) - Configures and deploys a WAR file to Tomcat

## Plugins

No external plugins. There is an internal [s6 module](polaris/deploy/plugins/modules/s6_service.py) that the [service_control](polaris/deploy/roles/service_control/README.md) role uses.

## Quick Start

Start by looking at [common](polaris/deploy/roles/common/README.md) as every role includes it. It defines many of the [defaults](polaris/deploy/roles/common/defaults/main.yml) that other roles use. If you want something to be picked up globally, you should define one of the values from this role. If you want something to be used only by a single role, you should define the role specific variable.

Next, [create_project_directories](polaris/deploy/roles/create_project_directories/README.md) is used to create the directory structure for a service. Other roles will require that this roll be called first.

After this, playbooks call various roles to add binaries, add the application files and configure their application as required.

## Related Products

* [NR Broker](https://github.com/bcgov/nr-broker)
* [NR Repository Composer](https://github.com/bcgov/nr-repository-composer)
* [Polaris Pipelines](https://github.com/bcgov-nr/polaris-pipelines)

## Development

Developing the roles requires having a machine avialable to target for Ansible. It is highly recommended that you use Vagrant to create a local virtual machine using the provided Vagrantfile. The local VM can be provisioned from scratch in a couple minutes.

In addition, application developers can use the Vagrant VM to test their playbooks. Most deployment issues can be resolved this way without needing to deploy to a real servers.

### Required

* [Vagrant](https://developer.hashicorp.com/vagrant)
* [VirtualBox](https://www.virtualbox.org) (on MacOS)

### Running development box

This will setup the development virtual machine. It will take some time to download the image and complete the setup.

```
vagrant up
```

### Copy files to development box

```
vagrant upload polaris
vagrant upload test polaris/deploy
```

### Use test playbooks

Connect to the virtual machine and then run the playbook. You can then check the state of the virtual machine and re-upload and re-run as needed.

```
vagrant ssh
cd polaris/deploy
export ANSIBLE_LIBRARY=/home/vagrant/polaris/deploy/plugins
ansible-playbook nodejs.yml
/apps_ux/sample/service/artifact/bin/nodejs/bin/node -v
curl localhost:8080
```

### Run an application playbook locally

```
vagrant up
vagrant upload polaris
cd <application root>
vagrant upload . polaris/app
```



### Why no container?

We don't provide a container image for use with Podman of Docker because applications are installed into a stateful server. Containers are setup to run a single executable with no system services (like ssh) avialable. They also have a simplified file system security model.

In the end, we want to mimic the server and not simply run the application. The VM created by Vagrant operates like a server in ways a container can not replicate.

# License

See: [LICENSE](./LICENSE)
