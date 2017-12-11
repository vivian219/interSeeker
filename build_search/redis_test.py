import redis

def test_():
    r=redis.Redis(host='127.0.0.1',port=6379)
    r.set('name','vivian')
    print(r.get('name'))
class RedisHelper:
    def __init__(self):
        self.__conn=redis.Redis(host='127.0.0.1')
        self.chan_sub='fm92.4'
        self.chan_pub='fm92.4'
    def public(self,msg):
        self.__conn.publish(self.chan_pub,msg)
        return True
    def subscribe(self):
        pub=self.__conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub
# subscribe
obj_sub=RedisHelper()
redis_sub=obj_sub.subscribe()

while True:
    msg=redis_sub.parse_response()
    print(msg)

#publish
obj_pub=RedisHelper()
obj_pub