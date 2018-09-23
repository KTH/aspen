__author__ = 'tinglev@kth.se'

import logging
from modules.steps.parse_stack_file import ParseStackFile
from modules.steps.parse_stack_path import ParseStackPath
from modules.steps.logging_policy_checker import LoggingPolicyChecker
from modules.steps.restart_policy_checker import RestartPolicyChecker
from modules.steps.resource_policy_checker import ResourcePolicyChecker
from modules.steps.parse_image_data import ParseImageData
from modules.steps.image_has_semantic_version import ImageHasSemanticVersion
from modules.steps.get_semantic_versions import GetSemanticVersions
from modules.steps.calculate_md5 import CalculateMd5
from modules.steps.cluster_verification import ClusterVerification
from modules.steps.init_service_pipeline_data import InitServicePipelineData
from modules.steps.calculate_semantic_version import CalculateSemanticVersion
from modules.steps.deploy_application import DeployApplication
from modules.steps.get_application_password import GetClusterLbIp
from modules.util.exceptions import (UnExpectedApplicationException,
                                     ExpectedApplicationException)
from modules.util import pipeline, data_defs

class DeploymentPipeline():

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.pipeline_data = {}
        self.pipeline_steps = pipeline.create_pipeline_from_array([
            ParseStackPath(),
            ClusterVerification(),
            ParseStackFile(),
            CalculateMd5(),
            LoggingPolicyChecker(),
            RestartPolicyChecker(),
            ResourcePolicyChecker(),
            InitServicePipelineData(),
            ParseImageData(),
            ImageHasSemanticVersion(),
            GetSemanticVersions(),
            CalculateSemanticVersion(),
            GetClusterLbIp(),
            DeployApplication()
        ])

    def set_pipeline_data(self, pipeline_data):
        self.pipeline_data = pipeline_data

    def run_pipeline(self):
        try:
            stack_file = self.pipeline_data[data_defs.STACK_FILE_PATH]
            self.log.info('Starting DeploymentPipline for file "%s"', stack_file)
            self.pipeline_steps[0].run_pipeline_step(self.pipeline_data)
        except UnExpectedApplicationException as ueae:
            pass
        except ExpectedApplicationException as eae:
            pass
        except Exception as ex:
            pass
