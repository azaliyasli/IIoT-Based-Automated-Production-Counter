import paho.mqtt.client as mqtt

class MQTTPublisher:
    def __init__(self, broker_address, port, topic):
        self.topic = topic
        self.client = mqtt.Client()
        self.client.connect(broker_address, port, 60)
        self.client.loop_start()

    def publish_count(self, count):
        self.client.publish(self.topic, str(count))

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()