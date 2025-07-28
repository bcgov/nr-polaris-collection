# self\_signed\_cert - Self-Signed Certificate Generation

This Ansible role generates a secure self-signed certificate, private key, and optional Java keystore for internal TLS or encryption purposes. It ensures secrets are generated only once per host using Ansible facts, and supports flexible formats like `pkcs12`.

## Role Variables

All variables are prefixed with `ssc_` to indicate they are specific to this role.

| Variable Name                 | Description                                                       | Default Value                                                                                      |
| ----------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `ssc_dir`                     | Directory where the certificate, key, and keystore will be stored | `{{ polaris_apps_service_install_home }}/.keys`                                                    |
| `ssc_user`                    | User who will own all generated files                             | `{{ polaris_install_user }}`                                                                       |
| `ssc_format`                  | Format of the certificate/keystore (`pkcs12`)              | `'pkcs12'`                                                                                         |
| `ssc_java_install`            | Whether to add the certificate to the Java trust store            | `"no"`                                                                                             |
| `ssc_java_home`               | Java installation path                                            | `{{ polaris_apps_service_install_home }}/bin/jdk`                                                  |
| `ssc_keystore`                | Path to the Java keystore (if used)                               | `{{ ssc_dir }}/key.jks`                                                                            |
| `ssc_key_filename`            | Filename of the private key                                       | `"key.pem"`                                                                                        |
| `ssc_key`                     | Full path to the private key                                      | `{{ ssc_dir }}/{{ ssc_key_filename }}`                                                             |
| `ssc_separate_key_pass`       | Whether the key uses a different password from the keystore       | `false`                                                                                            |
| `ssc_certificate_alias`       | Alias for the certificate in the keystore or Java trust store     | `{{ ansible_fqdn }}`                                                                               |
| `ssc_certificate_age`         | Number of days the certificate is valid                           | `3650`                                                                                             |
| `ssc_certificate_common_name` | Common Name (CN) used in the certificate subject                  | `{{ ansible_fqdn }}`                                                                               |
| `ssc_certificate_subject`     | Distinguished name for certificate subject                        | `/C=CA/ST=BC/L=Victoria/O=IMB/OU=CSNR/CN={{ ssc_certificate_common_name }}`                        |
| `ssc_certificate_options`     | OpenSSL options for certificate creation                          | `-x509 -sha256 -nodes -x509 -subj "{{ ssc_certificate_subject }}" -days {{ ssc_certificate_age }}` |
| `ssc_certificate_filename`    | Filename of the generated certificate                             | `'cert.pem'`                                                                                       |
| `ssc_certificate`             | Full path to the generated certificate                            | `{{ ssc_dir }}/{{ ssc_certificate_filename }}`                                                     |

> 🔐 Passwords for `ssc_keystore_pass` and `ssc_key_pass` are securely generated using the `password` lookup and stored via `set_fact` to ensure consistency during future runs.

## Role Behavior

* Validates the selected `ssc_format` is supported.
* Creates required directory with appropriate permissions.
* Dynamically generates secure passwords for keys and keystores.
* Includes format-specific certificate and key generation tasks (`pkcs12.yml`, etc.).
* Optionally installs the certificate into the Java trust store using `keytool`.

## Supported Formats

The role supports the following formats:

* `pkcs12`
* `pkcs8`
* `pkcs5`

## Dependencies

This role assumes:

* Default paths and user values are provided by a common role.
* `create_project_directories` has been executed beforehand to prepare the base structure.

## Installation Visualization

After execution, the file structure will resemble:

```
.
├── <polaris_apps_service_install_home>/
│   └── .keys/
│       ├── cert.pem
│       ├── key.pem
│       └── key.jks       # if applicable
```

## Example Playbook

```yaml
---
- hosts: all
  become: yes
  vars:
    polaris_apps_project_name: "test_project"
    polaris_apps_service_name: "test_service"
    polaris_apps_service_install_name: "v1"
  roles:
    - create_project_directories
    - self_signed_cert
```
