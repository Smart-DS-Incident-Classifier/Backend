from confluent_kafka import Consumer
from app.config import settings

consumer_config = {
    "bootstrap.servers": settings.kafka_broker,
    "group.id": "log-consumer-group",
    "auto.offset.reset": "earliest",
}

def consume_logs(topic: str):
    """Consume logs from Kafka."""
    consumer = Consumer(consumer_config)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                continue
            log_data = msg.value().decode("utf-8")
            print(f"Consumed log: {log_data}")
            # Add further processing logic here (e.g., save to DB)
    finally:
        consumer.close()
