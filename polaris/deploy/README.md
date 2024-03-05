# Ansible Collection - polaris.deploy

Documentation for the collection.

## Required Variables

| Variable | Example | Description |
| -------- | ------- | ----------- |
| `pd_prop_project_name` | RESULTS | Name of the project |
| `pd_prop_service_name` | results-war | Name of the service |
| `pd_prop_service_version` | 1.0.1 | The version of the service being deployed |
| `pd_prop_build_number` | 36 | The build number of the service being deployed |
| `artifactory_url` | https://bwa.nrs.gov.bc.ca/int/artifactory/ | URL to Ministry Artifact repository |
| `artifactory_username` | nrsci@bcgov |  |
| `artifactory_password` | **** | |

## Optional Variables

| Variable | Example | Description |
| -------- | ------- | ----------- |
| `pd_prop_project_id` | RESULTS | By default, the project id is the project name. This can be set to allow a single project/service to be deployed multiple times on one server |
| `pd_prop_service_id` | results-war | By default, the service id is the service name. This can be set to allow a single project/service to be deployed multiple times on one server |