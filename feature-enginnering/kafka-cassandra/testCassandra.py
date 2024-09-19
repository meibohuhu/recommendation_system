from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

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

finally:
    # Clean up and close the connection
    if cluster:
        cluster.shutdown()
    if session:
        session.shutdown()
