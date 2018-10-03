import atexit
import unittest
import requests
from pact import Consumer, Provider

pact = Consumer('deployment_poster').has_pact_with(Provider('reporting_provider'))
pact.start_service()
atexit.register(pact.stop_service)

class ReporterContract(unittest.TestCase):

    def test_post_deployment(self):
        expected_response = {}

        (pact
         .given('Reporter is running')
         .upon_receiving('a request for a deployment')
         .with_request(
             method='PUT',
             path='/api/v1/deployment',
             body=self.get_development_body(),
             headers={'Content-Type': 'application/json'})
         .will_respond_with(200, body=expected_response))

        with pact:
            result = requests.put('http://localhost:1234/api/v1/deployment', json={})

        self.assertEqual(result.json(), expected_response)

    def get_development_body(self):
        return {}
