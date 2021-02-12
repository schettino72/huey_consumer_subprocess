from huey.bin.huey_consumer import consumer_main

if __name__ == '__main__':
    # python my_consumer.py demo_tasks.huey -k process --disable_health_check --simple
    consumer_main()


