from kafka import KafkaProducer
from json import dumps
from time import sleep
import random
from datetime import datetime

def create_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

def generate_message():
    return {
        'user_id': str(random.sample([1, 2, 3, 4, 5], 1)[0]),
        'anime_id': str(random.sample([1, 2, 3], 1)[0]),
        'happened_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def main():
    producer = create_producer()
    topic = 'topic_133_mhu'
    
    try:
        while True:
            message = generate_message()
            future = producer.send(topic, value=message)
            record_metadata = future.get(timeout=10)
            
            print(f"Sent message: {message}")
            print(f"Topic: {record_metadata.topic}, "
                  f"Partition: {record_metadata.partition}, "
                  f"Offset: {record_metadata.offset}")
            
            sleep_ms = 1.0 * random.randint(0, 400)
            sleep(sleep_ms / 1000.0)
            
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        producer.close()

if __name__ == "__main__":
    main()