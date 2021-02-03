import singer
import tap_framework
import tap_chargebee.client
import tap_chargebee.streams
from tap_chargebee.streams.configurations import ConfigurationsStream

LOGGER = singer.get_logger()


class ChargebeeRunner(tap_framework.Runner):
    pass


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(
        required_config_keys=['api_key', 'start_date', 'site'])

    client = tap_chargebee.client.ChargebeeClient(args.config)

    runner = ChargebeeRunner(
        args, client, get_available_streams(args, client)
    )

    if args.discover:
        runner.do_discover()
    else:
        runner.do_sync()


if __name__ == '__main__':
    main()


def get_available_streams(self, cb_client):
    response = cb_client.make_request(
        url=ConfigurationsStream.get_url(self),
        method=ConfigurationsStream.API_METHOD)
    site_configurations = response['configurations']
    for site_config in site_configurations:
        if site_config.get('domain') == self.config.get('site'):
            product_catalog_version = site_config.get('product_catalog_version')
            if product_catalog_version == 'v2':
                available_streams = tap_chargebee.streams.ITEM_MODEL_AVAILABLE_STREAMS
                self.config['item_model'] = True
            elif product_catalog_version == 'v1':
                available_streams = tap_chargebee.streams.PLAN_MODEL_AVAILABLE_STREAMS
                self.config['item_model'] = False
    if self.config.get('item_model') is None:
        raise RuntimeError('Product Catalog version not defined')
    LOGGER.info("Model {}".format(self.config))
    return available_streams
