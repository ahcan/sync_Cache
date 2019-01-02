import redis
import settings

class Redit(object):
    def __init__(self, key):
        super(Redit, self).__init__()
        self.key = key
        POOL = redis.ConnectionPool(host=settings.REDIS['host'], 
                                    port=settings.REDIS['port'], 
                                    db=settings.REDIS['db'])
        self.conn = redis.Redis(connection_pool=POOL)

    def set_data(self, name, val):
        """
        retrun dict
        name: string is key to get value in main key
        """
        try:
            # return self.conn.hset(name= self.key, key = name, value = val)
            # print("name {0}".format(name))
            return self.conn.hmset(self.key, {'{0}'.format(name): val})
        except Exception as e:
            return str(e)

    def get_all(self):
        result = self.conn.hgetall(self.key)
        result = result if result else ''
        return result

    def get_data(self, name):
        """
        name is key to get data
        """
        result = self.conn.hget(name=self.key, key=name)
        result = result if result else ''
        return result