from .addons import AddonsStream
from .coupons import CouponsStream
from .customers import CustomersStream
from .events import EventsStream
from .invoices import InvoicesStream
from .payment_sources import PaymentSourcesStream
from .plans import PlansStream
from .subscriptions import SubscriptionsStream
from .transactions import TransactionsStream
from .virtual_bank_accounts import VirtualBankAccountsStream
from .credit_notes import CreditNoteStream
from .gifts import GiftsStream
from .orders import OrdersStream

AVAILABLE_STREAMS = [
    AddonsStream,
    CouponsStream,
    CreditNoteStream,
    CustomersStream,
    GiftsStream,
    InvoicesStream,
    OrdersStream,
    PaymentSourcesStream,
    PlansStream,
    SubscriptionsStream,
    TransactionsStream,
    EventsStream,
    VirtualBankAccountsStream
]
