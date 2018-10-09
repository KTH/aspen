__author__ = 'tinglev@kth.se'

from modules.util import data_defs, exceptions

def get_mock_deployment_json():
    return {
        "applicationName": "kth-azure-app",
        "cluster": "stage",
        "version": "1.3.4_abc123",
        "imageName": "kth-azure-app",
        "publishedUrl": "/kth-azure-app",
        "slackChannels": "#team-pipeline,#pipeline-logs",
        "publicNameSwedish": "Referensapplikation för våra kluster",
        "publicNameEnglish": "Reference application for our clusters",
        "descriptionSwedish": "En liten beskrivning",
        "descriptionEnglish": "A little description",
        "monitorUrl": "https://app-r.referens.sys.kth.se/_monitor",
        "created": "12519836591",
        "importance": "medium",
        "servicePath": "https://app-r.referens.sys.kth.se/kth-azure-app",
        "detectifyProfileTokens": "abc123,def456"
    }

def get_mock_deployment_error(expected=True):
    return exceptions.DeploymentError('This is a deployment error', expected=expected)

def get_image_data():
    return {
        data_defs.STACK_FILE_PATH: 'test/path/for/real/docker-stack.yml',
        data_defs.STACK_FILE_DIR_HASH: 'alejfbabovudbasepvbsoev',
        data_defs.APPLICATION_CLUSTER: 'stage',
        data_defs.APPLICATION_NAME: 'kth-azure-app',
        data_defs.SERVICES: [{
            data_defs.S_NAME: 'web',
            data_defs.S_IMAGE: {
                data_defs.IMG_NAME: 'kth-azure-app',
                data_defs.IMG_IS_SEMVER: False,
                data_defs.IMG_BEST_SEMVER_MATCH: None,
                data_defs.IMG_REGISTRY: 'kthregistryv2.sys.kth.se',
                data_defs.IMG_SEMVER_ENV_KEY: None,
                data_defs.IMG_SEMVER_VERSION: None,
                data_defs.IMG_TAGS: None,
                data_defs.IMG_VERSION: '2.0.1_abc123'
            },
            data_defs.S_LABELS: {
                'label1': 'value1,value11',
                'label2': 'value2'
            },
            data_defs.S_DEPLOY_LABELS: {
                'traefik.frontend.rule': 'PathPrefix:/kth-azure-app'
            }
        },
        {
            data_defs.S_NAME: 'api',
            data_defs.S_IMAGE: {
                data_defs.IMG_NAME: 'redis',
                data_defs.IMG_IS_SEMVER: True,
                data_defs.IMG_BEST_SEMVER_MATCH: '0.1.4_abc123',
                data_defs.IMG_REGISTRY: 'kthregistryv2.sys.kth.se',
                data_defs.IMG_SEMVER_ENV_KEY: 'API_VERSION',
                data_defs.IMG_SEMVER_VERSION: '~0.1.4',
                data_defs.IMG_TAGS: ['0.1.4_abc123', '0.1.3_123abc'],
                data_defs.IMG_VERSION: '${API_VERSION}'
            },
            data_defs.S_LABELS: {
                'label1': 'value12,value13',
                'label3': 'value3'
            }
        }]
    }

def get_parsed_stack_content():
    return {
        'services': {
            'web': {
                'environment': {
                    'ENV_KEY_1': 'ENV_VAL_1',
                    'WEB_VERSION': '~2.1.3_abc123'
                },
                'labels':{
                    'se.kth.slackChannels': '#pipeline',
                    'se.kth.importance': 'high'
                }
            },
            'api': {
                'image': 'test_registry/test_image:1.2.3_abc456',
                'environment': {
                    'API_KEY_1': 'API_VAL_1'
                },
                'logging': {
                    'options': {
                        'max-size': '10Mb',
                        'max-file': 10
                    }
                },
                'labels': {
                    'se.kth.slackChannels': '#team-pipeline,#ita-ops'
                },
                'deploy': {
                    'resources': {
                        'limits': {
                            'cpus': 0.5,
                            'memory': '100M'
                        },
                        'reservations': {
                            'cpus': 0.1,
                            'memory': '10M'
                        }
                    },
                    'restart_policy': {
                        'condition': 'on-failure',
                        'delay': '5s',
                        'max_attempts': 2
                    },
                    'labels': {
                        'traefik.deploy': 'true'
                    }
                }
            }
        }
    }

def get_cluster_ip_response():
    return [
        {
            'status': 'active',
            'name': 'everest-white',
            'lb_ip': '10.28.20.30:2376'
        },
        {
            'status': 'stage',
            'name': 'everest-black',
            'lb_ip': '10.28.21.30:2376'
        }
    ]

def get_tags_response():
    return {
        "name": "kth-azure-app",
        "tags": [
            "2.9.158_f9c44d7",
            "2.9.161_4754e4f",
            "2.9.184_974c427",
            "2.4.125_2a4f8a3",
            "2.7.84_d297141",
            "2.7.97_f1eafaf",
            "2.9.141_32f8c98",
            "2.9.152_651508d",
            "2.5.202_bc18537",
            "2.6.59_4c1def8",
            "2.8.118_f627d03",
            "2.8.122_8171648",
            "2.4.133_8b5ef50",
            "2.4.148_8b5ef50",
            "2.7.102_861cdf0",
            "2.8.131_6ceb6f6",
            "2.4.132_8b5ef50",
            "2.4.178_bd355c4",
            "2.6.55_4c1def8",
            "2.9.186_974c427",
            "2.7.108_f0cb388",
            "2.7.82_aff0d10",
            "2.8.115_f627d03",
            "2.8.125_d88802a",
            "2.4.123_2a4f8a3",
            "2.4.181_bd355c4",
            "2.4.186_599e682",
            "2.6.26_30636d1",
            "2.8.123_8171648",
            "2.8.124_787e8a9",
            "2.4.176_bd355c4",
            "2.4.185_bd355c4",
            "2.7.105_6752a41",
            "2.7.76_9a54a72",
            "2.4.137_8b5ef50",
            "2.4.145_8b5ef50",
            "2.4.175_bd355c4",
            "2.9.187_974c427",
            "2.7.83_3fad8be",
            "2.8.137_8e8a930",
            "2.9.178_7b6b15c",
            "2.9.198_7c0c3b7",
            "2.8.120_ffdb7fc",
            "2.9.157_fb67f00",
            "2.4.182_bd355c4",
            "2.6.50_7a37c74",
            "2.6.53_4c1def8",
            "2.7.80_d606c0f",
            "2.4.124_2a4f8a3",
            "2.7.89_31496ab",
            "2.8.109_eef42fc",
            "2.8.127_bccdcd6",
            "2.5.205_7f04afa",
            "2.6.52_4c1def8",
            "2.7.90_31496ab",
            "2.7.93_e8fe8a8",
            "2.6.41_7a37c74",
            "2.7.79_d606c0f",
            "2.8.119_dac3ed3",
            "2.9.153_5e510d6",
            "2.4.142_8b5ef50",
            "2.4.188_599e682",
            "2.6.28_30636d1",
            "2.9.145_89ee48a",
            "2.4.184_bd355c4",
            "2.6.18_22a065f",
            "2.4.128_2a4f8a3",
            "2.4.129_2a4f8a3",
            "2.4.170_bd355c4",
            "2.4.177_bd355c4",
            "2.6.71_64a99d5",
            "2.7.85_31496ab",
            "2.9.160_4754e4f",
            "2.4.189_599e682",
            "2.5.206_6b45aba",
            "2.6.20_22a065f",
            "2.6.67_4c1def8",
            "2.6.22_22a065f",
            "2.6.30_8827f86",
            "2.6.56_4c1def8",
            "2.6.66_4c1def8",
            "2.7.104_5c36db9",
            "2.7.86_31496ab",
            "2.9.146_ba33d15",
            "2.4.135_8b5ef50",
            "2.4.141_8b5ef50",
            "2.4.149_5b1e3fc",
            "2.6.33_05c5ddf",
            "2.4.187_599e682",
            "2.5.204_0ba03c8",
            "2.6.68_4c1def8",
            "2.8.117_f627d03",
            "2.4.121_efb1438",
            "2.4.127_2a4f8a3",
            "2.4.139_8b5ef50",
            "2.4.172_bd355c4",
            "2.8.133_d701331",
            "2.9.177_9a046a3",
            "2.5.10_6b45aba",
            "2.5.16_6b45aba",
            "2.6.24_5e6f2a8",
            "2.8.113_f4495c3",
            "2.9.144_a510734",
            "2.9.149_b03787f",
            "2.9.150_ba6ce2c",
            "2.4.174_bd355c4",
            "2.7.106_f0cb388",
            "2.7.98_f1eafaf",
            "2.8.111_f4495c3",
            "2.4.130_3001cc2",
            "2.4.179_bd355c4",
            "2.4.190_599e682",
            "2.4.194_b95601c",
            "2.4.193_b95601c",
            "2.5.12_6b45aba",
            "2.9.140_62637cc",
            "2.6.29_30636d1",
            "2.7.101_0f260fb",
            "2.8.110_f4495c3",
            "2.8.114_8dacac7",
            "2.4.120_efb1438",
            "2.4.134_8b5ef50",
            "2.4.147_8b5ef50",
            "2.5.11_6b45aba",
            "2.9.179_4c2ffb0",
            "2.9.202_3b01b96",
            "0.6.223_0119e3e",
            "2.5.15_6b45aba",
            "2.6.65_4c1def8",
            "2.7.88_31496ab",
            "2.7.107_f0cb388",
            "2.7.74_b590053",
            "2.7.77_7dfbae8",
            "2.9.142_89ee48a",
            "2.4.131_8b5ef50",
            "2.4.146_8b5ef50",
            "2.4.183_bd355c4",
            "2.6.51_b0b11f2",
            "2.9.148_b03787f",
            "2.6.27_30636d1",
            "2.7.78_d606c0f",
            "2.8.126_d88802a",
            "2.9.147_61f6759",
            "2.4.197_f9c287b",
            "2.5.13_6b45aba",
            "2.6.21_22a065f",
            "2.6.23_22a065f",
            "2.9.155_ceb1e6c",
            "2.9.159_8d98560",
            "2.5.203_f0b8a9e",
            "2.6.39_05c5ddf",
            "2.7.103_928ac07",
            "2.9.197_7c0c3b7",
            "2.8.121_43b6803",
            "2.9.200_3b01b96",
            "2.9.201_3b01b96",
            "2.5.9_6b45aba",
            "2.6.17_22a065f",
            "2.6.70_64a99d5",
            "2.7.75_f32f0e2",
            "2.4.191_b95601c",
            "2.4.199_f9c287b",
            "2.6.25_30636d1",
            "2.5.201_bc18537",
            "2.7.81_a13cb0d",
            "2.9.143_89ee48a",
            "2.4.200_f9c287b",
            "2.6.38_05c5ddf",
            "2.6.40_7a37c74",
            "2.8.132_d701331",
            "2.4.136_8b5ef50",
            "2.4.140_8b5ef50",
            "2.4.143_8b5ef50",
            "2.4.198_f9c287b",
            "2.9.156_6e42df6",
            "2.9.175_07f5d60",
            "2.4.180_bd355c4",
            "2.4.192_b95601c",
            "2.5.14_6b45aba",
            "2.6.42_7a37c74",
            "2.4.122_2a4f8a3",
            "2.4.126_2a4f8a3",
            "2.4.144_8b5ef50",
            "2.4.173_bd355c4",
            "2.7.87_31496ab",
            "2.9.151_709a100",
            "2.9.185_974c427"
        ]
    }
