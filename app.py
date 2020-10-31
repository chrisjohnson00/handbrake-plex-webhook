from flask import Flask, request
import json
import pygogo as gogo

application = Flask(__name__)
required_configs = []
# logging setup
kwargs = {}
formatter = gogo.formatters.structured_formatter
logger = gogo.Gogo('struct', low_formatter=formatter).get_logger(**kwargs)


@application.route('/')
def index():
    return 'Welcome to the Handbrake Plex Webhook Server!'


@application.route('/webhook', methods=['GET', 'POST'])
def web_hook():
    logger.info("Web hook called")
    info = request.form.to_dict()
    payload = info["payload"]
    # convert into JSON:
    json_payload = json.loads(payload)
    logger.info("Web hook JSON data", extra={'json': json_payload})
    logger.info("Interesting data", extra={'event': json_payload["event"],
                                           'user': json_payload["user"],
                                           'type': json_payload["Metadata"]["type"],
                                           'title': json_payload["Metadata"]["title"]})
    return 'Done'


@application.route('/health')
def health_check():
    # put logic here to ensure we are happy to fulfill user requests
    return "Success"


@application.route('/config')
def config():
    logger.info("Rendering config page")
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
