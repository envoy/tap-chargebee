from .addons import AddonsStream
from .coupons import CouponsStream
from .customers import CustomersStream
from .events import EventsStream
from .invoices import InvoicesStream
from .plans import PlansStream
from .subscriptions import SubscriptionsStream
from .transactions import TransactionsStream

AVAILABLE_STREAMS = [
    AddonsStream,
    CouponsStream,
    CustomersStream,
    InvoicesStream,
    PlansStream,
    SubscriptionsStream,
    TransactionsStream,
    EventsStream
]
