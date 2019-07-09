import requests
import json


def print_unexpected_json_error_key(key, server_answer, request_path, f=print):
    print_unexpected_json_error("field {} was not found".format(key), server_answer, request_path, f)


def print_unexpected_json_error(error, server_answer, request_path, f=print):
    f("Got unexpected json format: {}\n"
      "Request path: {}\n"
      "Message:\n'{}'".format(error, request_path, server_answer))


class ApiRequesterCommon:
    """Sends requests to REST API server"""

    def __init__(self, cfg):
        """

        :param cfg: ConfigReader instance, used to load configuration from config file
        :return: None
        """
        self.scheme = "http"

        self.address = cfg.get_value("address")
        self.port = cfg.get_value("port")

        self.username = cfg.get_value("username")
        self.password = cfg.get_value("password")

        self._authTokenPath = cfg.get_value("authTokenPath")
        self.timeout = cfg.get_value("serverDoesNotRespondTimeout")

        self.token = None
        # configure requests session
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def get(self, path):
        return self.server_request(path=path, method='GET')

    def put(self, path, data, eid=None):
        return self.server_request(path=path, data=data, eid=eid, method='PUT')

    def post(self, path, data):
        return self.server_request(path=path, data=data, method='POST')

    def patch(self, path, data, eid=None):
        return self.server_request(path=path, data=data, eid=eid, method='PATCH')

    def delete(self, path, eid=None):
        return self.server_request(path=path, eid=eid, method='DELETE')

    def server_request(self, path, scheme=None, address=None, port=None, data=None, put=False, eid=None, method=None):
        """
        Sends any type of request to server.

        There two ways to call this function: with 'method' param and without it.
        The one without 'method' param is deprecated and should not be used anymore. 'put' param is also deprecated

        :param path: request path
        :param scheme: scheme used for request, default used if not specified
        :param address: server address, default used if not specified
        :param port: server port, default used if not specified
        :param data: data for POST request, if equals None then GET request sent
        :param put: use put instead of post if True
        :param eid: if None then GET request, otherwise DELETE
        :param method: HTTP method specified as uppercase string (e.g. 'POST', 'GET', etc.)
        :return: string containing JSON server response
        """

        # TODO: move to compose_url method
        if scheme is None:
            scheme = self.scheme
        if address is None:
            address = self.address
        if port is None:
            port = self.port
        url = scheme + "://" + address + ":" + str(port) + path
        if eid is not None:
            url += "/" + str(eid) + "/"

        if self.token is None and path != self._authTokenPath:
            self.get_token()

        code = None
        answer = None
        try:
            if method is None:
                answer = self._deprecated_inner_request(url, data, eid, put)
            else:
                answer = self.session.request(method, url, data=data, timeout=self.timeout)
                if answer.status_code == 401:
                    self.get_token()
                    answer = self.session.request(method, url, data=data, timeout=self.timeout)
            code = answer.status_code
        except requests.Timeout:
            print("Timeout, server does not respond")
            exit(3)
        except requests.ConnectionError as error:    # TODO: catch other exceptions, if they exist
            print("Connection error occurred: %s. Exiting" % error)
            exit(3)

        if code < 200 or code >= 300:
            error_mesg = 'Api request "' + url + '"; http code: ' + str(code)
            if code == 500:
                filename = self._handle_code_500(answer.text)
                if filename:
                    error_mesg += '; server response saved to file: ' + filename
            elif code == 400:
                error_mesg += self._handle_code_400(answer.text)
            else:
                error_mesg += '; server response: ' + answer.text
                pass
            print(error_mesg)
            exit(2)       # fall with code 2 if something goes wrong
            # TODO: something different from just exit, maybe (if will need)

        return answer.text

    def _deprecated_inner_request(self, url, data, eid, put):
        if data is None:
            if eid is None:
                answer = self.session.get(url, timeout=self.timeout)
            else:
                answer = self.session.delete(url, timeout=self.timeout)
        else:
            if put:
                answer = self.session.put(url, timeout=self.timeout, data=data)
            else:
                answer = self.session.post(url, timeout=self.timeout, data=data)

        if answer.status_code == 401:  # first, try to get new token one time, if code == 401
            self.get_token()
            if data is None:
                if eid is None:
                    answer = self.session.get(url, timeout=self.timeout)
                else:
                    answer = self.session.delete(url, timeout=self.timeout)
            else:
                if put:
                    answer = self.session.put(url, timeout=self.timeout, data=data)
                else:
                    answer = self.session.post(url, timeout=self.timeout, data=data)
        return answer

    def _handle_code_500(self, server_response):
        """
        Handles 500 error code from server. Stores html server response to file

        :param server_response: answer from server
        :return: filename where stored serverResponse
        """
        filename = "server_error.html"
        try:
            with open(filename, 'w') as f:
                f.write(server_response)
        except IOError:
            print("Can not open file '%s' to write server answer. Skipping." % filename)
            return None
        return filename

    @staticmethod
    def _handle_code_400(text):
        """
        Handler for code 400 to override this function if needed and save reverse compatibility
        """
        return '; server response: ' + text

    def get_token(self):
        """
        Requests auth token from server and stores it

        :return: None
        """
        self.session.headers.pop("Authorization", None)     # delete old token if was

        data = json.dumps({"password": self.password, "username": self.username})
        answer = self.server_request(self._authTokenPath, data=data)

        try:
            self.token = json.loads(answer)["token"]
            self.session.headers.update({"Authorization": "Token " + self.token})
        except KeyError as err:
            print_unexpected_json_error_key(err, answer, self._authTokenPath)
            exit(1)
