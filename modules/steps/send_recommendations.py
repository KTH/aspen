__author__ = 'tinglev@kth.se'

import random
import requests
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, reporter_service, environment

class SendRecommendations(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT,
                data_defs.APPLICATION_NAME]

    def run_step(self, pipeline_data):
        parsed_data = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]
        application_name = pipeline_data[data_defs.APPLICATION_NAME]
        self.send_label_recommendations(application_name, parsed_data)
        return pipeline_data

    def send_label_recommendations(self, application_name, parsed_data):
        labels = [
            ('se.kth.publicName.english', 'My app name'),
            ('se.kth.publicName.swedish', 'Min apps namn'),
            ('se.kth.description.english', 'Short app description'),
            ('se.kth.description.swedish', 'Kort beskrivning av appen'),
            ('se.kth.importance', 'medium'),
            ('se.kth.detectify.profileToken', 'Profile token från Detectify')
        ]
        for label in labels:
            label_name = label[0]
            example_text = label[1]
            if not self.has_service_label(parsed_data, label_name):
                recommendation_text = self.create_recommendation_text(label_name, example_text)
                reporter_service.handle_recommendation(application_name, recommendation_text)

    def create_recommendation_text(self, label_name, example_value):
        return (f'{self.get_random_emoji()} {self.get_random_flavor_text()}\n '
                f'`{label_name}="{example_value}"`')

    def has_service_label(self, parsed_data, label_name):
        if 'services' in parsed_data:
            for _, service in parsed_data['services'].items():
                if 'labels' in service:
                    return label_name in service['labels']
                # Only try the first service
                return False
            return False

    def get_random_flavor_text(self):
        flavor_texts = [
            "Recommended docker-stack.yml config",
            "Improve your app by adding",
            "More awesomeness if you add",
            ":ingemar: Ingemar approves adding",
            "Psst dude you forgot",
            "Add this coizzle for massizzle iizzle",
            "... just add it and you will not see this again!",
            "All the cool kids have it",
            "Carl XVI tycker det blir mer kungligt om du addar",
            "Paddy slar mig pa kaften om du inte addar"
        ]

        return flavor_texts[random.randint(0, (len(flavor_texts) -1))]

    def get_random_emoji(self):

        emojis = [
            ":kissing_heart:",
            ":kissing_cat:",
            ":popcorn:",
            ":heart:",
            ":ok_hand:",
            ":+1:",
            ":sunglasses:",
            ":wink:",
            ":wink:",
            ":grinning:",
            ":ingemar:",
            ":first_place_medal:"
        ]
        
        return emojis[random.randint(0, (len(emojis) -1))]
