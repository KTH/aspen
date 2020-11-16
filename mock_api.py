__author__ = 'tinglev@kth.se'

from flask import Flask, jsonify
from test import mock_test_data # pylint: disable=C0411

app = Flask(__name__) # pylint: disable=C0103

@app.route("/tags/v2/kth-azure-app/tags/list")
def mock_tags():
    return jsonify(mock_test_data.get_tags_response())

@app.route("/tags/acr/v1/kth-azure-app/_tags")
def mock_azure_tags():
    return jsonify(mock_test_data.get_azure_tags_response())

@app.route("/clusters")
def mock_clusters():
    return jsonify(mock_test_data.get_cluster_ip_response())
