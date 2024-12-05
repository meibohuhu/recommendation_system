from redis import Redis

redis = Redis(host='localhost', port=6379, db=0)

all_values = redis.hgetall('recent_clicks:2')  # Returns {b'name': b'John', ...}

print(all_values)


# Use a pattern to find all keys starting with 'recent_clicks'
keys_to_delete = redis.keys('recent_clicks:*')   
print(keys_to_delete)

# # Delete all matching keys
# if keys_to_delete:
#     redis.delete(*keys_to_delete)      ## deletes all the keys in one command by unpacking the list of keys.
#     print(f"Deleted keys: {keys_to_delete}")
# else:
#     print("No keys found matching the pattern.")