import random
import time
from kafka import KafkaProducer
import json

def generate_sensor_data():
    return {
        "timestamp": time.time(),
        "temperature": random.uniform(20, 30),
        "humidity": random.uniform(30, 70),
        "soil_moisture": random.uniform(10, 50)
    }

def produce_messages(producer, topic, data):
    producer.send(topic, json.dumps(data).encode('utf-8'))

if __name__ == "__main__":
    kafka_topic = "agriculture"
    kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')

    while True:
        data = generate_sensor_data()
        produce_messages(kafka_producer, kafka_topic, data)
        time.sleep(5)  # Send data every 5 seconds
