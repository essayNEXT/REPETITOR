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
    Integer,
    OnDelete,
    OnUpdate,
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
    customer_type = ForeignKey(references=CustomerType)
    tlg_user_id = BigInt(
        null=False, unique=True
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
    context_type = ForeignKey(references=ContextType)
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
    text = Text(null=False)
    image = Varchar(null=True)
    sound = Varchar(null=True)
    is_active = Boolean(default=True)
    author = ForeignKey(
        references=Customer, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    context = ForeignKey(
        references=Context, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )


class Explanation(Table):
    """Describe explanation class."""

    id = UUID(primary_key=True)
    description = Varchar(null=False)
    explanation = Text(null=True)
    is_active = Boolean(default=True)


class RelationType(Table):
    """Describe relation type class."""

    id = UUID(primary_key=True)
    name = Varchar(length=30, null=False)
    description = Text(null=True)
    is_active = Boolean(default=True)


class ItemRelation(Table):
    """Describe item relation class."""

    id = UUID(primary_key=True)
    is_active = Boolean(default=True)
    author = ForeignKey(
        references=Customer, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    explanation = ForeignKey(
        references=Explanation, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    type = ForeignKey(
        references=RelationType, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )


class WrongAnswItem(Table):
    """Describe WrongAnswItem class."""

    id = UUID(primary_key=True)
    is_active = Boolean(default=True)
    relation = ForeignKey(
        references=ItemRelation, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    item = ForeignKey(
        references=Item, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )


class RightAnswItem(Table):
    """Describe RightAnswItem class."""

    id = UUID(primary_key=True)
    is_active = Boolean(default=True)
    relation = ForeignKey(
        references=ItemRelation, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    item = ForeignKey(
        references=Item, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )


class Question(Table):
    """Describe question class."""

    id = UUID(primary_key=True)
    is_active = Boolean(default=True)
    relation = ForeignKey(
        references=ItemRelation, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    item = ForeignKey(
        references=Item, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )


class Card(Table):
    """Describe cards class."""

    id = UUID(primary_key=True)
    repetition_level = Integer()
    memorization_stage = Integer()
    last_date = Timestamptz()
    is_active = Boolean(default=True)
    author = ForeignKey(
        references=Customer, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    user = ForeignKey(
        references=Customer, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    item_relation = ForeignKey(
        references=ItemRelation, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )


class ItemRelationView(Table):
    __tablename__ = "item_relation_view"

    item_relation = UUID(primary_key=True)
    item_text_1 = Text(length=255)
    item_author_1 = ForeignKey(
        references=Customer, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    item_context_name_short_1 = Varchar(length=10)
    question = ForeignKey(
        references=Question, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    right_answ_item = ForeignKey(
        references=RightAnswItem,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade,
    )
    item_text_2 = Text(length=255)
    item_author_2 = ForeignKey(
        references=Customer, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    item_context_name_short_2 = Varchar(length=10)
    is_active = Boolean(default=True)
