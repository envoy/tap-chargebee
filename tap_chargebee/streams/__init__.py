from .addons import AddonsStream
from .coupons import CouponsStream
from .customers import CustomersStream
from .events import EventsStream
from .invoices import InvoicesStream
from .payment_sources import PaymentSourcesStream
from .plans import PlansStream
from .subscriptions import SubscriptionsStream
from .transactions import TransactionsStream

AVAILABLE_STREAMS = [
    AddonsStream
    # CouponsStream,
    # CustomersStream,
    # InvoicesStream,
    # PaymentSourcesStream
    # PlansStream,
    # SubscriptionsStream,
    # TransactionsStream,
    # EventsStream
]
