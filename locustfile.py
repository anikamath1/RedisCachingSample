from locust import HttpUser, task, between
import time

class UserBehavior(HttpUser):
    wait_time = between(1, 2)  # wait between 1 and 2 seconds between each task

    @task
    def get_users_mysql(self):
        # This simulates a request to the /users-mysql endpoint
        with self.client.get("/users-mysql", catch_response=True) as response:
            if response.status_code == 200:
                print("Request to /users-mysql succeeded")
            else:
                print("Request to /users-mysql failed")

    @task
    def get_users_redis(self):
        # This simulates a request to the /users-redis endpoint
        with self.client.get("/users-redis", catch_response=True) as response:
            if response.status_code == 200:
                print("Request to /users-redis succeeded")
            else:
                print("Request to /users-redis failed")
