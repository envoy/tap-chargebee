from tap_chargebee.streams.base import BaseChargebeeStream


class CreditNoteStream(BaseChargebeeStream):
    TABLE = 'credit_notes'
    ENTITY = 'credit_note'
    KEY_PROPERTIES = ['id']
    BOOKMARK_PROPERTIES = ['updated_at']
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = ['updated_at']
    INCLUSION = 'available'
    SELECTED = True
    API_METHOD = 'GET'

    def get_url(self):
        return 'https://{}.chargebee.com/api/v2/credit_notes'.format(self.config.get('site'))
