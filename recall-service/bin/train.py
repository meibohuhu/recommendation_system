from pyspark.sql import SparkSession
from recall.dataset.anime import spark_load_ratings
from recall.model import item2vec
from recall.dataset import embedding
from recall.model.seq import simple_seq, deepwalk_seq


spark = SparkSession \
    .builder \
    .appName("concrec-recall") \
    .getOrCreate()

rating_df = spark_load_ratings(spark)
## DEEP WALK for list of anime_ids
anime_seq = deepwalk_seq.build_seq(rating_df, spark)   ## combine group of animes via animes rated by same user
print('sample gen done.' + anime_seq[0])

# word2vec => embeddings for items and users
(item_emb_df, user_emb_df) = item2vec.train_item2vec(anime_seq, rating_df)  ## via Word2Vec library
print('embedding trained.')

item_vec = item_emb_df.collect()
item_emb = {}
for row in item_vec:
    item_emb[row.word] = row.vector.toArray()

## Save into Redis
embedding.save_item_embedding(item_emb)
print(f'{len(item_emb)} Item embedding saved to redis.')

user_vec = user_emb_df.collect()
user_emb = {}
for row in user_vec:
    user_emb[row.user_id] = row.user_emb

embedding.save_user_embedding(user_emb)
print(f'{len(user_emb)} User embedding saved to redis.')

print('item2vec embedding done.')
item_redis = embedding.get_all_fields_from_items()
if item_redis:
    first_key, first_value = next(iter(item_redis.items()))  # Get the first (key, value) pair
    print(f"First element - Key: {first_key}, Value: {first_value}")
else:
    print("The dictionary is empty.")
