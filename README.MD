# Cloud Run Demo

This sample application consists of two services: a "markdown editor" and a separate "markdown renderer".  The editor sends post requests to the renderer.

Our loadgenerator sends a request even 5-10 seconds (with 10 users). We can control the error rate by submitting invalid requests to receieve a `400` error
or by submitting just the text `500` to get `500` errors.

Main services taken from <https://cloud.google.com/run/docs/tutorials/secure-services>.
