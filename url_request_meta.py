"""data model for a url with functions to check completeness and parse as curl."""


class UrlRequestMeta:

    def __init__(self, fullurl: str="", method: str = "GET", required_params: tuple = None, params: dict = None):

        self.fullurl = fullurl
        self.method = method
        self.required_params = required_params
        self.params = params


    @property
    def params_ready(self) -> bool:
        """returns whether all parameters are provided"""
        ...

    def create_url_string(self):
        """returns the url as url_encoded string.
        """
        ...

    def to_curl_string(self):
        """returns the curl command string that represents this request"""
