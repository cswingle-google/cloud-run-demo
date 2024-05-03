import os
from locust import HttpUser, task, between
import google.auth.transport.requests
import google.oauth2.id_token


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

    @task(os.getenv("ERROR_RATE", 1, type=int))
    def error_400(self):
        creds = self._get_creds()
        self.client.post(
            "/render", headers={"authorization": "Bearer " + creds}
        )

    @task(os.getenv("ERROR_RATE", 1, type=int))
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
        url = os.environ.get("FRONTEND_ADDR")
        if not url:
            raise Exception("FRONTEND_ADDR missing")
        request = google.auth.transport.requests.Request()

        return google.oauth2.id_token.fetch_id_token(request, url)
