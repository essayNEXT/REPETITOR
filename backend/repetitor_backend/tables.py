from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    UUID,
    Boolean,
    ForeignKey,
    BigInt,
    Email,
    Text,
    Timestamptz,
)


class CustomerType(Table):
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
    name = Varchar(length=50, null=False, unique=True)
    description = Varchar(length=200, null=False)
    is_active = Boolean(default=True, null=False)


class Customer(Table):
    """Describe user."""

    id = UUID(primary_key=True)
    customer_class = ForeignKey(references=CustomerType)
    tlg_user_id = BigInt(
        null=False
    )  # When we will add other frontend (not only Telegram,
    tlg_language = Varchar(lenght=10, null=False)  # this fields transform to null=True)
    tlg_user_name = Varchar(length=50, null=True)
    tlg_first_name = Varchar(length=50, null=False)
    tlg_last_name = Varchar(length=50, null=True)
    native_language = Varchar(length=10, null=True)
    first_name = Varchar(lenght=50, null=True)
    last_name = Varchar(lenght=50, null=True)
    email = Email(null=True)
    is_active = Boolean(default=True)


class ContextType(Table):
    """Describe content class."""

    id = UUID(primary_key=True)
    description = Text(null=False)
    name = Varchar(length=20, null=False, unique=True)
    is_active = Boolean(default=True)


class Context(Table):
    """Describe existing contents."""

    id = UUID(primary_key=True)
    context_class = ForeignKey(references=ContextType)
    name = Varchar(length=50, null=False)
    name_short = Varchar(length=10, null=False)
    description = Text(null=False)
    is_active = Boolean(default=True)


class CustomerContext(Table):
    """Describes all customer contexts."""

    id = UUID(primary_key=True)
    customer = ForeignKey(references=Customer)
    context_1 = ForeignKey(references=Context)
    context_2 = ForeignKey(references=Context)
    last_date = Timestamptz()
    is_active = Boolean(default=True)


class Item(Table):
    """Describe item class."""

    id = UUID(primary_key=True)
    author = ForeignKey(references=Customer)
    context = ForeignKey(references=Context)
    text = Text(null=False)
    image = Varchar(length=255, null=False)
    sound = Varchar(length=255, null=False)
    is_active = Boolean(default=True)


class RelationType(Table):
    """Describe relation type class."""

    id = UUID(primary_key=True)
    name = Varchar(length=50, null=False)
    description = Text(null=False)
    is_active = Boolean(default=True)


class Explanation(Table):
    """Describe explanation class."""

    id = UUID(primary_key=True)
    description = Varchar(length=50, null=False)
    explanation = Text(null=False)
    is_active = Boolean(default=True)


class ItemRelation(Table):
    """Describe ItemRelation class."""

    id = UUID(primary_key=True)
    author = ForeignKey(references=Customer)
    explanation = ForeignKey(references=Explanation)
    type = ForeignKey(references=RelationType)
    is_active = Boolean(default=True)


class WrongAnswItem(Table):
    """Describe WrongAnswItem class."""

    id = UUID(primary_key=True)
    relation = ForeignKey(references=ItemRelation)
    item = ForeignKey(references=Item)
    is_active = Boolean(default=True)


class RightAnswItem(Table):
    """Describe RightAnswItem class."""

    id = UUID(primary_key=True)
    relation = ForeignKey(references=ItemRelation)
    item = ForeignKey(references=Item)
    is_active = Boolean(default=True)


class Question(Table):
    """Describe question class."""

    id = UUID(primary_key=True)
    relation = ForeignKey(references=ItemRelation)
    item = ForeignKey(references=Item)
    is_active = Boolean(default=True)


class Card(Table):
    """Describe card class."""

    id = UUID(primary_key=True)
    user = ForeignKey(references=Customer)
    author = ForeignKey(references=Customer)
    relation = ForeignKey(references=ItemRelation)
    repetition_level = BigInt(null=False)
    last_data = Timestamptz(null=False)
    memorization_stage = BigInt(null=False)
    is_active = Boolean(default=True)
