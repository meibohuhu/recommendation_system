from kafka import KafkaConsumer, consumer
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

import json
import os
import datetime

KAFKA_TOPIC = 'views'
# Cassandra configuration
CASSANDRA_KEYSPACE = 'actions'
CASSANDRA_TABLE_VIEWS = 'views'
CASSANDRA_TABLE_CLICKS = 'clicks'

# Load secure connect bundle and token
cloud_config = {
    'secure_connect_bundle': 'secure-connect-concrec.zip'
}

# Initialize variables
auth_provider = None
cluster = None
session = None
try:
    # Load authentication credentials
    with open("recommendation_db-token.json") as f:
        secrets = json.load(f)
        CLIENT_ID = secrets.get("clientId")
        CLIENT_SECRET = secrets.get("secret")
        
        if not CLIENT_ID or not CLIENT_SECRET:
            raise ValueError("Client ID or secret is missing in the token file.")

except FileNotFoundError:
    print("Token file not found. Ensure 'recommendation_db-token.json' exists.")
    exit(1)
except json.JSONDecodeError:
    print("Error decoding the token JSON file. Ensure it's properly formatted.")
    exit(1)
except ValueError as e:
    print(e)
    exit(1)

try:
    # Initialize the authentication provider
    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    
    # Connect to the Cassandra cluster
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    # Execute a simple query to test the connection
    row = session.execute("SELECT release_version FROM system.local").one()
    if row:
        print(f"Cassandra version: {row[0]}")
    else:
        print("An error occurred while retrieving the version.")
        
except Exception as e:
    print(f"An error occurred while connecting to Cassandra: {e}")

# finally:
#     # Clean up and close the connection
#     if cluster:
#         cluster.shutdown()
#     if session:
#         session.shutdown()


def consume_kafka():
    print("Cassandra connected")
    # return 'OK'
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=['localhost:29092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='group-0',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    return consumer

for item in consume_kafka():
    # print(item)
    event = item.value
    print(event)
    if event.get('user_id') == None:   ## json get field
             continue;
    if event.get('anime_id') == None:   ## json get field
             continue;
    session.execute(
        f"""
        INSERT INTO actions.{KAFKA_TOPIC} (user_id, anime_id, happened_at)
        VALUES (%s, %s, %s)
        """,
        (
            int(event['user_id']),
            int(event['anime_id']),
            datetime.datetime.fromtimestamp(event['happened_at'])
        )
    )
