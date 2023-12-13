# /locustfile.py
from locust import HttpUser, task, between

class WebsiteTestUser(HttpUser):
    wait_time = between(1, 3) # task 사이 1 ~ 3초 랜덤 대기

    @task
    def my_task(self):
        self.client.get("/board") # test page 설정(end point)

"""
locustfile.py 위치에서 locust -f locustfile.py로 실행
이후 http://localhost:8089에서 locust 실행 - (http://0.0.0.0:8089)

"""