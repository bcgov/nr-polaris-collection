#!/usr/bin/env python




# https://skarnet.org/software/s6/s6-svc.html
# https://skarnet.org/software/s6/s6-svstat.html prints a short, human-readable or programmatically parsable summary of the state of a process monitored by s6-supervise.

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---

module: s6_service
short_description: A module to manage the state of services registered with Skarnet S6
description:
    - Manages the state of services that are already registered with S6.
    - This module will not create S6 service directories for you.
version_added: "2.3"
author: "Brenden Black (@ratioprosperous)"
        "DrydenLinden"
options:
    name:
        description:
            - Name of the service to manage. This must be the same name as your service directory.
        required: true
    state:
        description:
            - The state
        required: true
        choices: [ 'running', 'stopped', 'restarted' ]
        description:
            - C(running) and C(stopped) are idempotent actions that will not run commands unless necessary. C(restarted) will always cause a change on the target host.
    s6_home:
        description:
            - Where S6 is installed.
        required: false
        default: '/sw_ux/s6'
    scan_dir:
        description:
            - The directory S6 is using for its scan directory.
        required: false
        default: '/apps_ux/s6_services'
notes:
    - This module must be run as (i.e. C(become_user)) whatever user account s6 runs as
requirements:
    - Skarnet S6

'''



import os
import os.path
from ansible.module_utils.basic import AnsibleModule

class SkarnetS6(object):
    def __init__(self, module):
        self.module = module
        self.service = module.params['name']
        self.scan_dir = module.params['scan_dir']
        self.changed = False
        self.state = ''
        self.force = module.params['force']

        # TODO: fail if service/name is empty

        self.service_dir = self.scan_dir + '/' + self.service
        if (not os.path.exists(self.service_dir)):
            module.fail_json(msg="Unable to find %s" % self.service_dir)

        self.is_set_as_down = os.path.exists(self.service_dir + '/down')

        self.bin_dir = module.params['s6_home'] + '/bin'
        if (not os.path.exists(self.bin_dir)):
            module.fail_json(msg="Unable to find %s" % self.bin_dir)

        svstat = self.bin_dir + '/s6-svstat'
        svc = self.bin_dir + '/s6-svc'
        self.tools = { 'svstat': svstat, 'svc': svc  }
        # foreach tool in tools  module.fail_json(msg="Unable to locate %tool.key at %tool.value" % tool)

    def get_current_state(self):
        # /sw_ux/s6/bin/s6-svstat -up /apps_ux/s6_services/npe-e2edemo-war
        result = self.module.run_command("%s -up %s" % (self.tools['svstat'], self.service_dir), path_prefix=self.bin_dir)
        print("Executing command: %s -up %s" % (self.tools['svstat'], self.service_dir))
        self.module.debug(result)
        if (result[0] == 0):
            split = result[1].split()
            running = split[0].lower().endswith('true')
            return { 'running': running, 'pid': split[1] }
        else:
            if (self.force):
                # TODO
                self.module.warn(result[2])
                return { 'running': False, 'pid': -1 }
            else:
                self.module.warn(result[2])
                return { 'running': False, 'pid': -1 }

    def check_down(self):
        change = True
        result = ""
        result = self.module.run_command("rm down", cwd=self.service_dir)
        print("Executing command: rm down")
        if (result == ""):
            print ("Deleted down file")
            self.changed = True

    def stop(self):
        status = self.get_current_state()
        self.check_down()
        print("Service is running: %s" % status['running'])
        if (status['running']):
            # s6-svc -wd -d /apps_ux/s6_services/npe-e2edemo-war
            print("Executing command: sudo %s -wD -d %s" % (self.tools['svc'], self.service_dir))
            result = self.module.run_command("%s -wD -d %s" % (self.tools['svc'], self.service_dir), path_prefix=self.bin_dir)
            if (result[0] == 0):
                self.changed = True
                self.state = 'Stopping'
            else:
                self.module.fail_json(msg=result)
        else:
            self.state = 'Not running'

    def start(self):
        status = self.get_current_state()
        self.check_down()
        # if pid is -1, try to start supervisor (svc -a?)

        if (status['running']):
            self.state = 'Running'
        else:
            # s6-svc -wu -u /apps_ux/s6_services/npe-e2edemo-war
            print("still here")
            print("Executing command: %s -wu -u %s" % (self.tools['svc'], self.service_dir))
            result = self.module.run_command("%s -wu -u %s" % (self.tools['svc'], self.service_dir), path_prefix=self.bin_dir)
            if (result[0] == 0):
                self.changed = True
                self.state = 'Starting'
            else:
                print(result[0])
                self.module.fail_json(msg=result)


    def restart(self):
        status = self.get_current_state()
        self.check_down()
        if (status['running']):
            self.stop()
            self.start()
        else:
            self.start()

        # status = self.get_current_state()
        # if (status['running']):
            # print("Executing sudo %s -wD -d %s" % (self.tools['svc'], self.service_dir))
            # result = self.module.run_command("%s -wD -u %s" % (self.tools['svc'], self.service_dir), path_prefix=self.bin_dir)
            # self.state = 'Stopping'
            # if(result[0] == 0):
                # self.changed = True
                # self.start()
        # else:
            # self.start()

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            state=dict(choices=['running', 'stopped', 'restarted']),
            force=dict(required=False, default=False),
            s6_home=dict(required=False, default='/sw_ux/s6'),
            scan_dir=dict(required=False, default='/apps_ux/s6_services')
        ),
        supports_check_mode=False
    )
    s6 = SkarnetS6(module)

    desired_state = module.params['state']
    if (desired_state == 'stopped'):
        s6.stop()
    elif (desired_state == 'running'):
        s6.start()
    elif (desired_state == 'restarted'):
        s6.restart()
    else:
        module.fail_json(msg="desired state of '%s' is not supported" % desired_state)

    result = {}
    result['name'] = s6.service
    result['changed'] = s6.changed
    result['state'] = s6.get_current_state()


    module.exit_json(**result)


if __name__ == '__main__':
    main()
