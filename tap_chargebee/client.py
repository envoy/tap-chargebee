import time
import requests
import singer

from tap_framework.client import BaseClient


LOGGER = singer.get_logger()


class ChargebeeClient(BaseClient):

    def __init__(self, config, api_result_limit=100, include_deleted=True):
        super().__init__(config)

        self.api_result_limit = api_result_limit
        self.include_deleted = include_deleted
        self.user_agent = self.config.get('user_agent')

    def get_headers(self):
        headers = {}

        if self.config.get('user_agent'):
            headers['User-Agent'] = self.config.get('user_agent')

        return headers

    def get_params(self, params):

        if params is None:
            params = {}

        params['limit'] = self.api_result_limit
        params['include_deleted'] = self.include_deleted

        return params

    def make_request(self, url, method, params=None, base_backoff=15,
                     body=None):

        if params is None:
            params = {}

        LOGGER.info("Making {} request to {}".format(method, url))

        response = requests.request(
            method,
            url,
            auth=(self.config.get("api_key"), ''),
            headers=self.get_headers(),
            params=self.get_params(params),
            json=body)

        # Handle Rate Limiting (429)
        if response.status_code == 429:
            if base_backoff > 120:
                raise RuntimeError('Backed off too many times, exiting!')

            LOGGER.warn('Got a 429, sleeping for {} seconds and trying again'
                        .format(base_backoff))

            time.sleep(base_backoff)

            return self.make_request(url, method, base_backoff * 2, body)

        if response.status_code != 200:
            raise RuntimeError(response.text)

        return response.json()
