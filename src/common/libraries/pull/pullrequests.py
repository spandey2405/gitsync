import os
from src.common.libraries.runshellcommand import run_command
from django.conf import settings
gitsys_settings = settings.GIT_SYNC_DIRECTORY

class PullRequest():

    def execute(self, options):
        print options
        selected_code_base = gitsys_settings[options['code_base']]
        dir = selected_code_base['dir']
        branch = selected_code_base['branch'][options['stage']]
        command = "cd {0} && git stash && git pull origin {1} && git stash pop".format(dir, branch)
        try:
            response = run_command(command)
            print response
        except Exception as e:
            print e
            response = False
        self.runprocess(selected_code_base['process'])
        return response


    def runprocess(self, process):

        for event in process:
            event = event.split('.')
            process_name = event[0]
            process_info = settings.GIT_SYNC_PROCESS[process_name]

            module = process_info['module_name']
            type   = process_info['type']
            print module, type
            if type == "SysVinit":
                command = "Service {0} restart".format(module)
            else:
                command = "restart {0}".format(module)

            print command

        return True


