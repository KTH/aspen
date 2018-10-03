__author__ = 'tinglev'

from abc import ABCMeta, abstractmethod
import time
import os
import logging
import subprocess
from modules.util import exceptions, reporter_service

class BasePipelineStep:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.log = logging.getLogger(self.get_step_name())
        self.next_step = None

    @abstractmethod
    def run_step(self, pipeline_data): #pragma: no cover
        """ Should return pipeline_data """
        pass

    @abstractmethod
    def get_required_env_variables(self): #pragma: no cover
        """ Should return a string array with the names of the environment
            variables required by the current step """
        pass

    @abstractmethod
    def get_required_data_keys(self): #pragma: no cover
        """ Should return a string array with the names of the keys
            that has to exist and have values in the data-object that
            is passed between build steps """
        pass

    def get_step_name(self):
        return self.__class__.__name__

    def has_missing_step_data(self, data):
        for key in self.get_required_data_keys():
            if not data or not key in data:
                return key
        return None

    def has_missing_environment_data(self):
        for env in self.get_required_env_variables():
            if not env in os.environ:
                return env
            if not os.environ.get(env):
                self.log.warning('Environment variable "%s" exists but is empty', env)
        return None

    def run_pipeline_step(self, pipeline_data):
        step_data_missing = self.has_missing_step_data(pipeline_data)
        environment_missing = self.has_missing_environment_data()
        self.check_environment_missing(pipeline_data, environment_missing)
        self.check_step_data_missing(pipeline_data, step_data_missing)
        self.log.debug('Running "%s"', self.get_step_name())
        try:
            self.run_step(pipeline_data)
        except Exception as ex: # pylint: disable=W0703
            self.handle_pipeline_error(ex, pipeline_data)
        if self.next_step:
            self.next_step.run_pipeline_step(pipeline_data)
        return pipeline_data

    def check_environment_missing(self, pipeline_data, environment_missing):
        if environment_missing:
            self.log.error('Step environment missing "%s" for step "%s", and pipeline_data "%s"',
                           environment_missing, self.get_step_name(), pipeline_data)
            raise exceptions.DeploymentError('Step environment not ok',
                                             pipeline_data=pipeline_data,
                                             step_name=self.get_step_name())

    def check_step_data_missing(self, pipeline_data, step_data_missing):
        if step_data_missing:
            self.log.error('Step data "%s" missing for step "%s", and pipeline_data "%s"',
                           step_data_missing, self.get_step_name(), pipeline_data)
            raise exceptions.DeploymentError('Step pipeline_data not ok',
                                             pipeline_data=pipeline_data,
                                             step_name=self.get_step_name())

    def handle_pipeline_error(self, error, pipeline_data):
        msg = str(error)
        if isinstance(error, subprocess.CalledProcessError):
            msg = str(error.output) # pylint: disable=E1101
        if not isinstance(error, exceptions.DeploymentError):
            # Convert all exceptions to deployment errors
            error = exceptions.DeploymentError(msg)
            # Mark them as unexpected
            error.expected = False
        # Complement error with step data
        error = self.add_error_data(error, pipeline_data)
        self.log.debug('An error occured: "%s"', str(error))
        reporter_service.handle_deployment_error(error)
        self.stop_pipeline()

    def add_error_data(self, deployment_error, pipeline_data):
        deployment_error.pipeline_data = pipeline_data
        deployment_error.step_name = self.get_step_name()
        if deployment_error.retryable:
            deployment_error.timestamp = time.time()
        return deployment_error

    def set_next_step(self, next_step):
        self.next_step = next_step
        return next_step

    def stop_pipeline(self):
        self.log.info('Stopped pipeline at step "%s"', self.get_step_name())
        self.next_step = None
