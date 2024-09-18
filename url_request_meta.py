"""data model for a url with functions to check completeness and parse as curl."""
from urllib import parse

from urllib3 import request, BaseHTTPResponse


class UrlRequestMeta:

    def __init__(self, fullurl: str="", method: str = "GET", params: dict = None, required_params: tuple = None):
        """constructor method of a url meta instance

        :param fullurl: the full url including the schema and any endpoint
        :param method: the http method (GET, POST) as string
        :param required_params: list if required parameters. This is used to check if the url meta is complete
          or to update the parameter set from a set of other parameters that may contain other  keys as well
        :param params: the initial parameters to start with."""

        self.fullurl = fullurl
        self.method = method
        self.params = params or {}
        self.required_params = required_params or tuple()

    @property
    def params_ready(self) -> bool:
        """returns whether all parameters are provided"""
        for key in self.required_params:
            if not self.params.get([key]): return False
        return True

    def update_params(self, param_dict: dict):
        """extracts keys from the dictionary that match the required parameters"""
        for key, value in param_dict.items():
            if key in self.required_params or len(self.required_params) == 0:
                self.params[key] = value

    def create_url_string(self) -> str:
        """returns the url as url_encoded string.
        """
        return self.fullurl + "?" + parse.urlencode(self.params)

    def __call__(self) -> BaseHTTPResponse:
        """makes a request using the url meta"""

        return request(method=self.method, url=self.fullurl,  headers={"content-type": "application/json"}, json=self.params)

    def to_curl_string(self) -> str:
        """returns the curl command string that represents this request"""
        param_strings = [f'-d "{key}={value}"' for key, value in self.params.items()]
        s = "curl -X {method} {url} " + " ".join(param_strings)
        return s.format(method=self.method, url=self.fullurl)