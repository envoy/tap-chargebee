from tap_chargebee.streams.base import BaseChargebeeStream


class CouponCodesStream(BaseChargebeeStream):
    TABLE = 'coupon_codes'
    ENTITY = 'coupon_code'
    KEY_PROPERTIES = ['code']
    BOOKMARK_PROPERTIES = []
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = []
    INCLUSION = 'available'
    SELECTED = True
    API_METHOD = 'GET'

    def get_url(self):
        return 'https://{}.chargebee.com/api/v2/coupon_codes'.format(self.config.get('site'))
