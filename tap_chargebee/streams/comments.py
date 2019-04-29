from tap_chargebee.streams.base import BaseChargebeeStream


class CommentsStream(BaseChargebeeStream):
    TABLE = 'comments'
    ENTITY = 'comment'
    KEY_PROPERTIES = ['id']
    BOOKMARK_PROPERTIES = []
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = []
    INCLUSION = 'available'
    SELECTED = True
    API_METHOD = 'GET'

    def get_url(self):
        return 'https://{}.chargebee.com/api/v2/comments'.format(self.config.get('site'))
