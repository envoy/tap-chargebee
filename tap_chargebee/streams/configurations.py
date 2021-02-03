from tap_chargebee.streams.base import BaseChargebeeStream


class ConfigurationsStream(BaseChargebeeStream):
    API_METHOD = 'GET'

    def get_url(self):
        return 'https://{}.chargebee.com/api/v2/configurations'.format(self.config.get('site'))
