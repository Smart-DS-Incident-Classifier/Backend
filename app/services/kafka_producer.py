from confluent_kafka import Producer
import json
from app.config import settings

producer_config = {"bootstrap.servers": settings.kafka_broker}  # Update with your Kafka server
producer = Producer(producer_config)

def produce_log(topic: str, log_data: dict):
    """Send a log to Kafka."""
    try:
        producer.produce(topic, key=str(log_data.get("source", "unknown")), value=json.dumps(log_data))
        producer.flush()
    except Exception as e:
        print(f"Error producing log: {e}")
