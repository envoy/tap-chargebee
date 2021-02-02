import singer
import tap_framework
import tap_chargebee.client
import tap_chargebee.streams
from tap_chargebee.streams.plans import PlansStream

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
    AVAILABLE_STREAMS = tap_chargebee.streams.PLAN_MODEL_AVAILABLE_STREAMS
    self.config['item_model'] = False
    # temporary API to check Item model
    response = cb_client.make_request(
        url=PlansStream.get_url(self),
        method=PlansStream.API_METHOD)

    if 'api_error_code' in response.keys():
        if response['api_error_code'] == 'configuration_incompatible':
            AVAILABLE_STREAMS = tap_chargebee.streams.ITEM_MODEL_AVAILABLE_STREAMS
            self.config['item_model'] = True
    return AVAILABLE_STREAMS
