"""VerifyDeploymentSuccess

After deploying a docker stack, this step performs docker service ls commands
for a configurable amount of times with a configurable amount of delay in between
to see that all replicas of the services have been deployed. In case of a timeout
the step will report an error with the output from a docker ps command"""

__author__ = 'tinglev@kth.se'

import re
import time
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, regex, process, exceptions, environment

class VerifyDeploySuccess(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)
        self.wait_seconds = environment.get_with_default_int(
            environment.VERIFY_START_DELAY_SECS, 5
            )
        self.wait_times = environment.get_with_default_int(
            environment.VERIFY_START_RETRY_TIMES, 5
            )

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.DEPLOY_OUTPUT, data_defs.DOCKER_HOST_IP]

    def run_step(self, pipeline_data):
        skip_deployment = environment.get_env(environment.SKIP_DEPLOYMENT)
        if skip_deployment:
            return pipeline_data
        service_names = self.get_all_service_names(pipeline_data)
        if not service_names:
            raise exceptions.DeploymentError(f'Couldnt get service names from deployment '
                                             f'output. Output was: '
                                             f'"{pipeline_data[data_defs.DEPLOY_OUTPUT]}"')
        for service in service_names:
            self.wait_for_service_replication(pipeline_data, service)
        return pipeline_data

    def get_ps_output(self, pipeline_data, service):
        cluster_lb_ip = pipeline_data[data_defs.DOCKER_HOST_IP]
        output = process.run_with_output(f'DOCKER_TLS_VERIFY=1 docker -H {cluster_lb_ip} '
                                         f'service ps --no-trunc {service}')
        return output.decode('utf-8')

    def wait_for_service_replication(self, pipeline_data, service):
        for i in range(self.wait_times):
            self.log.debug('Checking if service "%s" has all replicas (attempt #%s/#%s)',
                           service, i+1, self.wait_times)
            match = self.get_running_replicas(pipeline_data, service)
            if match.group(1) == match.group(2):
                self.log.debug('Service "%s" has %s/%s replicas. All clear.',
                               service, match.group(1), match.group(2))
                break
            self.log.debug('Service "%s" only at %s/%s replicas, waiting %s secs',
                           service, match.group(1), match.group(2), self.wait_seconds)
            time.sleep(self.wait_seconds)
        else:
            msg = (f'Application didnt start correctly. Service ps output is: \n'
                   f'\n{self.get_ps_output(pipeline_data, service)}\n')
            raise exceptions.DeploymentError(msg)

    def get_running_replicas(self, pipeline_data, service):
        service_ls = self.run_service_ls(pipeline_data, service).split('\n')
        for line in service_ls:
            match = re.match(regex.get_nr_of_replicas(), line)
            if match:
                return match
        raise exceptions.DeploymentError('Could not find any service when running ls')

    def get_all_service_names(self, pipeline_data):
        output_rows = pipeline_data[data_defs.DEPLOY_OUTPUT].split('\n')
        service_names = []
        for row in output_rows:
            match = re.match(regex.get_service_name_from_create_deploy(), row)
            if not match:
                match = re.match(regex.get_service_name_from_update_deploy(), row)
            if match:
                self.log.debug('Got service "%s" for deployment', match.group(1))
                service_names.append(match.group(1))
        return service_names

    def run_service_ls(self, pipeline_data, service):
        cluster_lb_ip = pipeline_data[data_defs.DOCKER_HOST_IP]
        output = process.run_with_output(f'DOCKER_TLS_VERIFY=1 docker -H tcp://{cluster_lb_ip} '
                                         f'service ls --filter name={service}')
        return output.decode('utf-8')
