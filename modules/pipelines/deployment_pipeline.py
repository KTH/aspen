__author__ = 'tinglev@kth.se'

import logging
from modules.steps.parse_stack_file import ParseStackFile
from modules.steps.parse_stack_path import ParseStackPath
from modules.steps.logging_policy_checker import LoggingPolicyChecker
from modules.steps.restart_policy_checker import RestartPolicyChecker
from modules.steps.resource_policy_checker import ResourcePolicyChecker
from modules.steps.parse_image_data import ParseImageData
from modules.steps.image_has_semantic_version import ImageHasSemanticVersion
from modules.steps.get_image_tags import GetImageTags
from modules.steps.calculate_md5 import CalculateMd5
from modules.steps.cluster_verification import ClusterVerification
from modules.steps.init_service_pipeline_data import InitServicePipelineData
from modules.steps.calculate_semantic_version import CalculateSemanticVersion
from modules.steps.deploy_application import DeployApplication
from modules.steps.get_docker_host_ip import GetDockerHostIp
from modules.steps.secret_verification import SecretVerification
from modules.steps.get_application_password import GetApplicationPassword
from modules.steps.docker_compose_validate import DockerComposeValidate
from modules.steps.get_cache_entry import GetCacheEntry
from modules.steps.write_cache_entry import WriteCacheEntry
from modules.steps.first_conditional_stop import FirstConditionalStop
from modules.steps.decrypt_app_secrets import DecryptAppSecrets
from modules.steps.verify_deploy_success import VerifyDeploySuccess
from modules.steps.remove_error_cache_entry import RemoveErrorCacheEntry
from modules.steps.report_success import ReportSuccess
from modules.steps.second_conditional_stop import SecondConditionalStop
from modules.steps.verify_pipeline_data import VerifyPipelineData
from modules.steps.verify_frontend_rule import VerifyFrontendRule
from modules.steps.stop_excluded_apps import StopExcludedApps
from modules.steps.volume_step import VolumeStep
from modules.util import pipeline, data_defs, exceptions, reporter_service

class DeploymentPipeline():

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.pipeline_data = {}
        self.pipeline_steps = []
        self.init_steps()

    def init_steps(self):
        self.pipeline_steps = pipeline.create_pipeline_from_array([
            ParseStackPath(),
            ClusterVerification(),
            StopExcludedApps(),
            GetCacheEntry(),
            CalculateMd5(),
            ParseStackFile(),
            InitServicePipelineData(),
            ParseImageData(),
            VerifyPipelineData(),
            VerifyFrontendRule(),
            ImageHasSemanticVersion(),
            # Stop if is_semver == false and md5_cache == md5_local
            FirstConditionalStop(),
            GetImageTags(),
            CalculateSemanticVersion(),
            # Stop if local best match == cache best match and md5_cache == md5_local
            SecondConditionalStop(),
            DockerComposeValidate(),
            GetApplicationPassword(),
            SecretVerification(),
            LoggingPolicyChecker(),
            RestartPolicyChecker(),
            ResourcePolicyChecker(),
            DecryptAppSecrets(),
            VolumeStep(),
            GetDockerHostIp(),
            DeployApplication(),
            # Run when tests are added to test_complete_pipeline and integration_tests
            VerifyDeploySuccess(),
            WriteCacheEntry(),
            RemoveErrorCacheEntry(),
            ReportSuccess()
        ])

    def set_pipeline_data(self, pipeline_data):
        self.pipeline_data = pipeline_data

    def run_pipeline(self):
        try:
            stack_file = self.pipeline_data[data_defs.STACK_FILE_PATH]
            self.log.debug('Starting DeploymentPipline for file "%s"', stack_file)
            pipeline_data = self.pipeline_steps[0].run_pipeline_step(self.pipeline_data)
            return pipeline_data
        except exceptions.DeploymentError as dep_err:
            self.log.error(('Deployment error in step "%s" '
                            'with pipeline_data "%s" '
                            'and message: "%s"'),
                           dep_err.step_name, dep_err.pipeline_data, str(dep_err))
            reporter_service.handle_deployment_error(dep_err)
