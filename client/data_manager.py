import requests

class DataManager():
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.request_url = self.server_ip + "/generate_images"

    def request_generate(self, text):
        request_url = self.request_url + "/" + text
        response = requests.post(request_url)
        status_code = response.status_code
        if status_code != 200:
            print("Error with", status_code)
            return "error"
        else:
            return response
