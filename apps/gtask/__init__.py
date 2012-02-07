import redis
import simplejson as json


REDIS_SERVER = {
    'default': {
        'host': '127.0.0.1',
        'port': '6379',
        'username': '',
        'password': '',
    }
}


class RedisServer(object):

    def __init__(self):
        db = 'default' 
        host = REDIS_SERVER[db]['host']
        port = int(REDIS_SERVER[db]['port'])

        self.cn = redis.StrictRedis(host=host, port=port, db=db)
        self.key = None

    def get_task_logs(self, key, num=25):
        self.key = 'log-%s' % (key,)
        log = []
        for i in self.cn.lrange(self.key, 0, num):
            i = eval(i)
            log.append(i)

        return log