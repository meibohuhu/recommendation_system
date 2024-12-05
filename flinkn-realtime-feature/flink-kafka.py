from pyflink.common import Types, Configuration, Row
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.time_characteristic import TimeCharacteristic
from pyflink.table import StreamTableEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.table.schema import Schema
from pyflink.table.window import Tumble
from pyflink.table import expressions as expr
from pyflink.datastream.functions import MapFunction

from redis import Redis


import json

redis = Redis(host='localhost', port=6379, db=0)

class JsonToRowMapFunction(MapFunction):
    def __init__(self):
        self.type_info = Types.ROW_NAMED(
            ['user_id', 'anime_id', 'happened_at'],
            [Types.STRING(), Types.STRING(), Types.STRING()]
        )

    def map(self, json_str):
        try:
            print(f"Received message: {json_str}")
            data = json.loads(json_str)
            return Row(
                user_id=str(data.get('user_id')),
                anime_id=str(data.get('anime_id')),
                happened_at=data.get('happened_at')
            )
        except Exception as e:
            print(f"Error processing message: {e}, input: {json_str}")
            return None

    def get_type_info(self):
        return self.type_info

def datastream_api_demo():
    # 1. Create configuration
    config = Configuration()
    jar_path = "file:/Users/wendyhu/Project/recommendation_system/recommendation_system/flinkn-realtime-feature/flink-sql-connector-kafka-3.3.0-1.20.jar"   ## download connector to local
    config.set_string("pipeline.jars", jar_path)

    # 2. Create execution environment
    env = StreamExecutionEnvironment.get_execution_environment(config)
    table_env = StreamTableEnvironment.create(env)
    env.set_parallelism(1)

    # 3. Kafka properties for localhost
    properties = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'topic_133_mhu_group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': 'false'
    }
    print('create kafka consumer')
    # 4. Create Kafka consumer
    kafka_consumer = FlinkKafkaConsumer(
        topics='topic_133_mhu',
        deserialization_schema=SimpleStringSchema(),
        properties=properties
    )
    kafka_consumer.set_start_from_earliest()
    # 5. Create data stream with JsonToRowMapFunction
    json_map = JsonToRowMapFunction()
    ds = env.add_source(kafka_consumer)\
        .map(json_map, output_type=json_map.get_type_info())\
        .filter(lambda x: x is not None)

    # 6. Convert stream to table
    schema = Schema.new_builder() \
        .column('user_id', 'STRING') \
        .column('anime_id', 'STRING') \
        .column('happened_at', 'STRING') \
        .column_by_expression('rowtime', 'CAST(happened_at AS TIMESTAMP(3))') \
        .watermark('rowtime', 'rowtime - INTERVAL \'5\' SECOND') \
        .build()

    t = table_env.from_data_stream(ds, schema)
    t.print_schema()

    # 7. Process stream: Groups the data by the defined window (w) and the user_id field. Each combination of user_id and the tumbling window is treated as a group.
    res_table = t \
        .window(Tumble.over(expr.lit(60).seconds).on(t.rowtime).alias('w')) \
        .group_by(expr.col('w'), expr.col('user_id')) \
        .select(
            expr.col('w').start.alias('start_t'),
            expr.col('user_id'),
            expr.col('anime_id').collect
        ) \
        .execute()

    # 8. Save results to Redis
    redis_prefix = 'recent_clicks'
    with res_table.collect() as results:
        for result in results:
            user_id = result[1]
            clicks = result[2]
            print(f'user: {user_id}, clicks: {clicks}')
            redis.hset(f'{redis_prefix}:{user_id}', mapping=clicks)

    # 9. Execute the job
    env.execute('User Clicks Analysis')

if __name__ == "__main__":
    try:
        datastream_api_demo()
    except Exception as e:
        print(f"Error in application: {str(e)}")
        raise