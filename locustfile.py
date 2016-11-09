"""
This is a very basic testsuite for testing the API. Testing the UI
isn't being considered so far.
"""

from locust import HttpLocust, TaskSet, task

API_BASE = '/api'


class UserBehavior(TaskSet):
    def get(self, location):
        api_url = API_BASE + location
        self.client.get(api_url)

    @task(3)
    def zero_results_search(self):
        self.get("/search/?format=json&search=test")

    @task(3)
    def results_search(self):
        self.get("/search/?format=json&search=digital")

    @task(2)
    def index(self):
        self.get("/search/")

    # def profile(self):
    #     self.get("/profile")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
