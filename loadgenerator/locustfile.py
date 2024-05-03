import os
from locust import HttpUser, task, between


class EditorLoadUser(HttpUser):
    wait_time = between(5, 10)
    error_rate = os.getenv("ERROR_RATE", 1)

    @task(2)
    def reload_index(self):
        creds = self._get_creds()
        self.client.get("/", headers={"authorization": "Bearer " + creds})

    @task(10)
    def sucessful_render(self):
        creds = self._get_creds()
        self.client.post(
            "/render",
            json={"data": "**Hello, world!**"},
            headers={"authorization": "Bearer " + creds},
        )

    @task(int(os.getenv("ERROR_RATE", 1)))
    def error_400(self):
        creds = self._get_creds()
        self.client.post(
            "/render", headers={"authorization": "Bearer " + creds}
        )

    @task(int(os.getenv("ERROR_RATE", 1)))
    def error_500(self):
        creds = self._get_creds()
        self.client.post(
            "/render",
            json={"data": "500"},
            headers={"authorization": "Bearer " + creds},
        )

    def on_start(self):
        creds = self._get_creds()
        self.client.get("/", headers={"authorization": "Bearer " + creds})

    def _get_creds(self):
        return os.popen("gcloud auth print-identity-token").read().strip()
