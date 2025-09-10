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

# NR Polaris Ansible Collection Development

Developing the roles requires having a machine available to target with Ansible. It is highly recommended to use Vagrant to create a local virtual machine using the provided Vagrantfile. The local VM can be provisioned from scratch in a couple of minutes.

In addition, application developers can use the Vagrant VM to test their playbooks. Most deployment issues can be resolved this way without needing to deploy to real servers.

## Required

* [Vagrant](https://developer.hashicorp.com/vagrant)
* [VirtualBox](https://www.virtualbox.org) (on macOS)

## Why no container?

We do not provide a container image for use with Podman or Docker because applications are installed into a stateful server. Containers are set up to run a single executable with no system services (like SSH) available. They also have a simplified file system security model.

In the end, we want to mimic the server and not simply run the application. The VM created by Vagrant operates like a server in ways a container cannot replicate.

## Running the development box

This will set up the development virtual machine. It will take some time to download the image and complete the setup.

```
vagrant up
```

This setups the vagrant user to be able to use systemd and sets the following env:

```
ANSIBLE_LIBRARY=/home/vagrant/polaris/deploy/plugins
```

You now have a running provisioned vm that you can connect to using `vagrant ssh`.

## Upload collection to the development box

Precondition: Running provisioned vm

This first step in all of the following examples is to upload the polaris collection to the vagrant vm.

```
vagrant ssh -c 'rm -r polaris'
vagrant upload -c polaris
```

By default, the `upload` command merges the files in the path. It is recommended that you clear out the polaris folder and start from scratch whenever you want to upload a new playbook as the existing files in `polaris/deploy` may conflict.

### Use test playbooks

Precondition: Upload collection

This will upload the test playbooks to the vm.

```
vagrant upload test polaris/deploy
```

Next, connect to the virtual machine and run the test playbooks. You can then check the state of the virtual machine, re-upload files, and re-run as needed. Some examples using the test playbooks are shown next.

#### Test playbooks - Install nodejs

Precondition: Upload collection and test playbooks

```
vagrant ssh
cd ~/polaris/deploy
ansible-playbook nodejs.yml
/apps_ux/sample/service/artifact/bin/nodejs/bin/node -v
# curl app -- port may be different if multiple apps installed
curl localhost:8080
```
#### Test playbooks - control app

Precondition: Upload collection, test playbooks and install app (example assumes test playbook's nodejs)

This shows how to stop an application.

```
vagrant ssh
cd ~/polaris/deploy
# Test service control stop (Change action/var as needed)
ansible-playbook -e service_control_var=nodejs \
  -e service_control_action=stop \
  servicectrl.yml
# curl app -- port may be different if multiple apps installed (fail expected)
curl localhost:8080
```

If you change the `service_control_action` to `start` then the app should come back.

## Copy app playbook and install - NodeJs

Precondition: Copy collection

```
vagrant upload <application root>/playbooks polaris/deploy
vagrant upload overlay_nodejs polaris/deploy
vagrant ssh
mkdir -p polaris/app
cd polaris/app
oras pull ghcr.io/bcgov/nr-nodejs-sample/package:v3.2.0
cd ../deploy
ansible-playbook -e env_vars=vagrant playbook.yaml
```

## Copy app playbook and install - Java

Precondition: Copy collection

```
vagrant upload <application root>/playbooks polaris/deploy
vagrant upload overlay_java polaris/deploy
vagrant ssh
mkdir -p /ansible/downloads
cd /ansible/downloads
sudo curl -L -H "Authorization: token ${GH_TOKEN}" \
  https://maven.pkg.github.com/bcgov/java-maven-pipeline-example/bcgov/example/java-maven-pipeline-example/1.0.1-main-SNAPSHOT/java-maven-pipeline-example-1.0.1-main-20250818.180118-27.war \
  -o java-maven-pipeline-example.war
cd ~/polaris/deploy
ansible-playbook -e env_vars=vagrant playbook.yaml
```

# License

See: [LICENSE](./LICENSE)
