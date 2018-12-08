import paho.mqtt.publish
import os
import json

# https://pypi.org/project/paho-mqtt/#single


def publish(topic, **kwargs):
    kwargs.setdefault("hostname", os.environ["MQTT_HOST"])
    kwargs.setdefault(
        "auth",
        {"username": os.environ["MQTT_USER"], "password": os.environ["MQTT_PASS"]},
    )
    if "json" in kwargs:
        kwargs["payload"] = json.dumps(kwargs.pop("json"))
    paho.mqtt.publish(topic, **kwargs)
