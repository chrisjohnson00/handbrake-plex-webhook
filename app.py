from flask import Flask, request
import logging
import json

application = Flask(__name__)
application.logger.setLevel(logging.INFO)
required_configs = []


@application.route('/')
def index():
    return 'Welcome to the Handbrake Plex Webhook Server!'


@application.route('/webhook', methods=['GET', 'POST'])
def web_hook():
    application.logger.info("Web hook called")
    application.logger.info("Web hook headers: {}".format(request.headers))
    info = request.form.to_dict()
    payload = info["payload"]
    # convert into JSON:
    json_payload = json.loads(payload)
    application.logger.info("json payload {}".format(json_payload))
    application.logger.info(
        "Interesting data - Event: '{}' User: '{}' Type: '{}' Title: '{}'".format(json_payload["event"],
                                                                                  json_payload["user"],
                                                                                  json_payload["Metadata"]["type"],
                                                                                  json_payload["Metadata"]["title"]))
    return 'Done'


@application.route('/health')
def health_check():
    # put logic here to ensure we are happy to fulfill user requests
    return "Success"


@application.route('/config')
def config():
    application.logger.info("Rendering config page")
    response_text = ""
    for config in required_configs:
        value = application.config.get(config)
        if any(secret in config for secret in ['KEY', 'TOKEN', 'PASSWORD']):
            response_text += "{}: [REDACTED]<br/>".format(config)
        else:
            response_text += "{}: {}<br/>".format(config, value)
    return response_text


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
