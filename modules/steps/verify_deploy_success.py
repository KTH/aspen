__author__ = 'tinglev@kth.se'

import re
import time
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, regex, process, exceptions

class VerifyDeploySuccess(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.DEPLOY_OUTPUT, data_defs.CLUSTER_LB_IP]

    def run_step(self, pipeline_data):
        service_names = self.get_all_service_names(pipeline_data)
        for service in service_names:
            self.wait_for_service_replication(pipeline_data, service)
        return pipeline_data

    def wait_for_service_replication(self, pipeline_data, service):
        for _ in range(5):
            self.log.debug('Checking if service "%s" has all replicas', service)
            service_ls = self.run_service_ls(pipeline_data, service).split('\n')
            for line in service_ls:
                match = re.match(regex.get_nr_of_replicas(), line)
                if match:
                    break
            else:
                raise exceptions.DeploymentError('Could not find any service when running ls')
            if match.group(1) == match.group(2):
                # All replicas up
                self.log.debug('Service "%s" has %s/%s replicas, continuing',
                                service, match.group(1), match.group(2))
                break
            self.log.debug('Service "%s" only at %s/%s replicas, waiting 5 secs',
                            service, match.group(1), match.group(2))
            time.sleep(5)
        else:
            raise exceptions.DeploymentError('Missing at least one service replica')

    def get_all_service_names(self, pipeline_data):
        output_rows = pipeline_data[data_defs.DEPLOY_OUTPUT].split('\n')
        service_names = []
        for row in output_rows:
            match = re.match(regex.get_service_name_from_deploy(), row)
            if match:
                self.log.debug('Got service "%s" for deployment', match.group(1))
                service_names.append(match.group(1))
        return service_names

    def run_service_ls(self, pipeline_data, service):
        cluster_lb_ip = pipeline_data[data_defs.CLUSTER_LB_IP]
        return process.run_with_output(f'docker -H {cluster_lb_ip} '
                                       f'service ls --filter name={service}')
