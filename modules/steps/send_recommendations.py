__author__ = 'tinglev@kth.se'

import random
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, reporter_service, pipeline_data_utils

class SendRecommendations(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT,
                data_defs.APPLICATION_NAME]

    def run_step(self, pipeline_data):
        self.send_label_recommendations(pipeline_data)
        return pipeline_data

    def send_label_recommendations(self, pipeline_data):
        application_name = pipeline_data[data_defs.APPLICATION_NAME]
        labels = [
            ('se.kth.publicName.english', 'This apps name'),
            ('se.kth.publicName.swedish', 'Denna applikations namn'),
            ('se.kth.description.english', 'Short app description'),
            ('se.kth.description.swedish', 'Kort beskrivning av applikationen'),
            ('se.kth.importance', 'Övervakningsvikt. Värden: low, medium eller high.'),
            ('se.kth.detectify.profileToken', 'Profile token från Detectify')
        ]
        for label in labels:
            label_name = label[0]
            example_text = label[1]
            if not self.has_service_label(pipeline_data, label_name):
                print("{} - Missing label '{}'".format(data_defs.APPLICATION_NAME, label_name))
                recommendation_text = self.create_recommendation_text(label_name, example_text)
                reporter_service.handle_recommendation(pipeline_data,
                                                       application_name,
                                                       recommendation_text)
            else:
                print("{} - Got label '{}'".format(data_defs.APPLICATION_NAME, label_name))


    def create_recommendation_text(self, label_name, example_value):
        return (f'{self.get_random_emoji()} {self.get_random_flavor_text()}\n '
                f'`{label_name}="{example_value}"`')

    def has_service_label(self, pipeline_data, label_name):
        for _, service in pipeline_data_utils.get_parsed_services(pipeline_data):
            if 'labels' in service:
                return label_name in [label.split('=')[0] for label in service['labels']]
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
