import redis
import time
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_LIST = "mylist"

def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    while True:
        # Here, we're just counting items in the list, but you can expand this to process and remove items if desired.
        list_length = r.llen(REDIS_LIST)
        print(f"Items in list {REDIS_LIST}: {list_length}")
        time.sleep(10)

if __name__ == "__main__":
    main()