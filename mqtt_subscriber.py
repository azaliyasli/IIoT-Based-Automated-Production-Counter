import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    data = message.payload.decode('utf-8')
    print(f"Content: {message.topic} | Total Bottles: {data}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
broker_address = "broker.hivemq.com"
port = 1883

print(f"⏳ Connecting to {broker_address}...")

try:
    client.connect(broker_address, port, 60)
    client.subscribe("factory/line1/bottle_count")
    print("✅ Connection success, listening...")
    client.loop_forever()
except Exception as e:
    print(f"❌ Conncetion failed: {e}")