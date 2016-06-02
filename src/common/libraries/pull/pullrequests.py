import os
from src.common.libraries.runshellcommand import run_command
from django.conf import settings
gitsys_settings = settings.GIT_SYNC_DIRECTORY

class PullRequest():

    def execute(self, options):
        response = dict()
        selected_code_base = gitsys_settings[options['code_base']]
        dir = selected_code_base['dir']
        branch = selected_code_base['branch'][options['stage']]
        command = "cd {0} && git stash && git pull origin {1} && git stash pop".format(dir, branch)
        try:
            response['pull_request'] = run_command(command)
        except Exception as e:
            print e
            response = False
        response['process'] = self.runprocess(selected_code_base['process'])
        return response


    def runprocess(self, process):
        response = dict()
        for event in process:
            event = event.split('.')
            process_name = event[0]
            process_info = settings.GIT_SYNC_PROCESS[process_name]

            module = process_info['module_name']
            type   = process_info['type']
            if type == "SysVinit":
                command = "Service {0} restart".format(module)
            else:
                command = "restart {0}".format(module)

            response[process_name] = run_command(command)

        return response


