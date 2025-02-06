# NR Polaris Collection

The Ansible collection of pipeline is for deploying applications to NR servers.

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
