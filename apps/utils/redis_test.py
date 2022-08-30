import redis
import time

r = redis.Redis(host='localhost', port=6379, password='123456.',db=0, charset="utf8", decode_responses=True)
r.set("mobile", "123")

# 配置1秒之后过期
r.expire("mobile", 1)
print(r.get("mobile"))

time.sleep(1)
print(r.get("mobile"))
