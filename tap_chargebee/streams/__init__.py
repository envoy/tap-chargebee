from .addons import AddonsStream
from .coupons import CouponsStream
from .credit_notes import CreditNotesStream
from .customers import CustomersStream
from .events import EventsStream
from .invoices import InvoicesStream
from .payment_sources import PaymentSourcesStream
from .plans import PlansStream
from .subscriptions import SubscriptionsStream
from .transactions import TransactionsStream
from .virtual_bank_accounts import VirtualBankAccountsStream

AVAILABLE_STREAMS = [
    AddonsStream,
    CouponsStream,
    CreditNotesStream,
    CustomersStream,
    InvoicesStream,
    PaymentSourcesStream,
    PlansStream,
    SubscriptionsStream,
    TransactionsStream,
    EventsStream,
    VirtualBankAccountsStream
]
