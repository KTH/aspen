__author__ = 'tinglev'

from abc import ABCMeta, abstractmethod
import os
import logging
import subprocess
from modules.util import exceptions

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

    def step_data_is_ok(self, data):
        for key in self.get_required_data_keys():
            if not data or not key in data:
                return False
        return True

    def step_environment_ok(self):
        for env in self.get_required_env_variables():
            if not env in os.environ:
                return False
            if not os.environ.get(env):
                self.log.warning('Environment variable "%s" exists but is empty', env)
        return True

    def run_pipeline_step(self, data):
        if not self.step_environment_ok():
            self.log.error('Step environment not ok for step "%s", and pipeline_data "%s"',
                           self.get_step_name(), data)
            raise exceptions.DeploymentError('Step environment not ok',
                                             pipeline_data=data,
                                             step_name=self.get_step_name())
        if not self.step_data_is_ok(data):
            self.log.error('Step data not ok for step "%s", and pipeline_data "%s"',
                           self.get_step_name(), data)
            raise exceptions.DeploymentError('Step pipeline_data not ok',
                                             pipeline_data=data,
                                             step_name=self.get_step_name())
        self.log.debug('Running "%s"', self.get_step_name())
        try:
            self.run_step(data)
        except exceptions.DeploymentError as de_err:
            # Complement error with step data
            de_err.pipeline_data = data
            de_err.step_name = self.get_step_name()
            raise
        except Exception as ex:
            msg = str(ex)
            if isinstance(ex, subprocess.CalledProcessError):
                msg = str(ex.output) # pylint: disable=E1101
            de_err = exceptions.DeploymentError(msg,
                                                pipeline_data=data,
                                                step_name=self.get_step_name())
            raise de_err
        if self.next_step:
            self.next_step.run_pipeline_step(data)
        return data

    def set_next_step(self, next_step):
        self.next_step = next_step
        return next_step

    def stop_pipeline(self):
        self.log.info('Stopped pipeline at step "%s"', self.get_step_name())
        self.next_step = None
