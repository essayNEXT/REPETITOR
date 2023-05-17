from piccolo.table import Table
from piccolo.columns import Varchar, UUID, Boolean, ForeignKey, BigInt


class CustomerClass(Table):
    """Describe type of possible users:
    
    for example:
    - 'regular user' - ordinary consumer of the service, registered and unprivileged
    - 'trusted user' - a user whose information entered can be used by other users without
    restrictions (for example - Google, Microsoft - when we receive a translation about their services)
    - 'teacher user' - a user who has the status of a teacher: that is, the information entered by him
    can be shown to individual users (if there is a mutual fixed consent)
    ...
    """
    id = UUID(primary_key=True)
    name = Varchar(length=50, null=False)
    describe = Varchar(length=200, null=False)
    is_active = Boolean(default=True, null=False)


class Customer(Table):
    """Describe user."""

    id = UUID(primary_key=True)
    customer_class = ForeignKey(references=CustomerClass)
    telegram_user_id = BigInt(null=False)               # When we will add other frontend (not only Telegram,
    telegram_language = Varchar(lenght=3, null=False)   # this fields transform to null=True)
    user_name = Varchar(length=50, null=True)
    first_name = Varchar(length=50, null=False)
    last_name = Varchar(length=50, null=True)
    is_active = Boolean(default=True)
