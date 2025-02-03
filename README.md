# NR Polaris Collection

The Ansible collection of pipeline is for deploying applications to NR servers.

# Local Development

```
vagrant upload polaris
vagrant upload test polaris/deploy
vagrant ssh
cd polaris/deploy
ansible-playbook nodejs.yml
/apps_ux/sample/service/artifact/bin/nodejs/bin/node -v
```

# License

See: [LICENSE](./LICENSE)
