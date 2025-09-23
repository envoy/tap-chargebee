import singer
import datetime

from dateutil.parser import parse
from tap_framework.streams import BaseStream
from tap_framework.config import get_config_start_date
from tap_chargebee.state import get_last_record_value_for_table, incorporate, \
    save_state

LOGGER = singer.get_logger()


class BaseChargebeeStream(BaseStream):

    def write_schema(self):
        singer.write_schema(
            self.catalog.stream,
            self.catalog.schema.to_dict(),
            key_properties=self.catalog.key_properties,
            bookmark_properties=self.BOOKMARK_PROPERTIES)

    def generate_catalog(self):
        schema = self.get_schema()
        mdata = singer.metadata.new()

        metadata = {
            "selected": self.SELECTED,
            "inclusion": self.INCLUSION,
            "valid-replication-keys": self.VALID_REPLICATION_KEYS,
            "selected-by-default": self.SELECTED_BY_DEFAULT,
            "schema-name": self.TABLE
        }

        for k, v in metadata.items():
            mdata = singer.metadata.write(
                mdata,
                (),
                k,
                v
            )

        for field_name, field_schema in schema.get('properties').items():
            inclusion = 'available'

            if field_name in self.KEY_PROPERTIES:
                inclusion = 'automatic'

            mdata = singer.metadata.write(
                mdata,
                ('properties', field_name),
                'inclusion',
                inclusion
            )

        return [{
            'tap_stream_id': self.TABLE,
            'stream': self.TABLE,
            'key_properties': self.KEY_PROPERTIES,
            'bookmark_properties': self.BOOKMARK_PROPERTIES,
            'schema': self.get_schema(),
            'metadata': singer.metadata.to_list(mdata)
        }]

    # This overrides the transform_record method in the Fistown Analytics tap-framework package
    def transform_record(self, record):
        with singer.Transformer(integer_datetime_fmt="unix-seconds-integer-datetime-parsing") as tx:
            metadata = {}

            if self.catalog.metadata is not None:
                metadata = singer.metadata.to_map(self.catalog.metadata)

            return tx.transform(
                record,
                self.catalog.schema.to_dict(),
                metadata)

    def get_stream_data(self, data):
        entity = self.ENTITY
        return [self.transform_record(item.get(entity)) for item in data]

    def sync_data(self):
        table = self.TABLE
        api_method = self.API_METHOD
        done = False

        # Attempt to get the bookmark date from the state file (if one exists and is supplied).
        LOGGER.info('Attempting to get the most recent bookmark_date for entity {}.'.format(self.ENTITY))
        bookmark_date = get_last_record_value_for_table(self.state, table, 'bookmark_date')

        # If there is no bookmark date, fall back to using the start date from the config file.
        if bookmark_date is None:
            LOGGER.info('Could not locate bookmark_date from STATE file. Falling back to start_date from config.json instead.')
            bookmark_date = get_config_start_date(self.config)
        else:
            bookmark_date = parse(bookmark_date)

        # Convert bookmarked start date to POSIX.
        bookmark_date_posix = int(bookmark_date.timestamp())

        # Create params for filtering
        if self.ENTITY == 'event':
            params = {"occurred_at[after]": bookmark_date_posix}
            bookmark_key = 'occurred_at'
        else:
            params = {"updated_at[after]": bookmark_date_posix}
            bookmark_key = 'updated_at'

        LOGGER.info("Querying {} starting at {}".format(table, bookmark_date))

        while not done:
            max_date = bookmark_date

            response = self.client.make_request(
                url=self.get_url(),
                method=api_method,
                params=params)

            to_write = self.get_stream_data(response.get('list'))

            with singer.metrics.record_counter(endpoint=table) as ctr:
                singer.write_records(table, to_write)

                ctr.increment(amount=len(to_write))

                for item in to_write:
                    max_date = max(
                        max_date,
                        parse(item.get(bookmark_key))
                    )

            self.state = incorporate(
                self.state, table, 'bookmark_date', max_date)

            if not response.get('next_offset'):
                LOGGER.info("Final offset reached. Ending sync.")
                done = True
            else:
                LOGGER.info("Advancing by one offset.")
                params['offset'] = response.get('next_offset')
                bookmark_date = max_date

        save_state(self.state)
