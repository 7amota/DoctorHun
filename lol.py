from redis import Redis
redis_host = '127.0.0.1'
r = Redis(redis_host, socket_connect_timeout=1) # short timeout for the test

r.ping() 

print('connected to redis "{}"'.format(redis_host))