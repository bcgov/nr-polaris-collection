# NR Polaris Collection

The Ansible collection of pipeline is for deploying applications to NR servers.

## Roles

- [Common Role](polaris/deploy/roles/common/README.md)
- [Create Project Directories Role](polaris/deploy/roles/create_project_directories/README.md)
- [JDK Role](polaris/deploy/roles/jdk/README.md)
- [Node.js Role](polaris/deploy/roles/nodejs/README.md)
- [Node.js App Role](polaris/deploy/roles/nodejs_app/README.md)
- [Patch Intention Role](polaris/deploy/roles/patch_intention/README.md)
- [Port Manager Role](polaris/deploy/roles/port_manager/README.md)
- [Self Signed Cert Role](polaris/deploy/roles/self_signed_cert/README.md)
- [Service Control Role](polaris/deploy/roles/service_control/README.md)
- [Tomcat Role](polaris/deploy/roles/tomcat/README.md)
- [Webade Connection Jar Role](polaris/deploy/roles/webade_connection_jar/README.md)
- [Webapp Role](polaris/deploy/roles/webapp/README.md)

## Development

Required:

* [Vagrant](https://developer.hashicorp.com/vagrant)
* [VirtualBox](https://www.virtualbox.org)

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
```

# License

See: [LICENSE](./LICENSE)
