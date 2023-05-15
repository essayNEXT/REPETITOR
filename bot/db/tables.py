from piccolo.table import Table
from piccolo.columns import UUID, Varchar, Boolean, BigInt, Integer, ForeignKey, OnDelete, OnUpdate, Text, Timestamptz


class UserClass(Table):
    id = UUID(primary_key=True)
    name = Varchar(length=30, null=False)
    is_active = Boolean(default=True)


class Users(Table):
    id = UUID(primary_key=True)
    telegram_user_id = BigInt(null=False, unique=True, index=True)
    telegram_language = Varchar(length=10, null=False)
    user_name = Varchar(length=30, null=False)
    first_name = Varchar(length=30, null=False)
    last_name = Varchar(length=30, null=False)
    is_active = Boolean(default=True)
    user_class = ForeignKey(
        references=UserClass,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
        )


class ContextClass(Table):
    id = UUID(primary_key=True)
    name = Varchar(length=30, null=False)
    description = Text(null=True)
    is_active = Boolean(default=True)


class Context(Table):
    id = UUID(primary_key=True)
    name = Varchar(length=30, null=False)
    name_alfa2 = Varchar(length=30)
    description = Text(null=True)
    is_active = Boolean(default=True)
    context_class = ForeignKey(
        references=ContextClass,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )


class Item(Table):
    id = UUID(primary_key=True)
    text = Text(null=False)
    image = Varchar(null=True)
    sound = Varchar(null=True)
    is_active = Boolean(default=True)
    author = ForeignKey(
        references=Users,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
        )
    context = ForeignKey(
        references=Context,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )


class Explanation(Table):
    id = UUID(primary_key=True)
    description = Varchar(null=False)
    explanation = Text(null=True)
    is_active = Boolean(default=True)


class RelationType(Table):
    id = UUID(primary_key=True)
    name = Varchar(length=30, null=False)
    description = Text(null=True)
    is_active = Boolean(default=True)


class ItemRelation(Table):
    id = UUID(primary_key=True)
    is_active = Boolean(default=True)
    author = ForeignKey(
        references=Users,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
        )
    explanation = ForeignKey(
        references=Explanation,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )
    type = ForeignKey(
        references=RelationType,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )


class WrongAnswItem(Table):
    id = UUID(primary_key=True)
    is_active = Boolean(default=True)
    relation = ForeignKey(
        references=ItemRelation,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
        )
    item = ForeignKey(
        references=Item,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )


class RightAnswItem(Table):
    id = UUID(primary_key=True)
    is_active = Boolean(default=True)
    relation = ForeignKey(
        references=ItemRelation,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
        )
    item = ForeignKey(
        references=Item,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )


class Question(Table):
    id = UUID(primary_key=True)
    is_active = Boolean(default=True)
    relation = ForeignKey(
        references=ItemRelation,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
        )
    item = ForeignKey(
        references=Item,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )


class Cards(Table):
    id = UUID(primary_key=True)
    repetition_level = Integer()
    memorization_stage = Integer()
    last_date = Timestamptz()
    is_active = Boolean(default=True)
    author = ForeignKey(
        references=Users,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
        )
    user = ForeignKey(
        references=Users,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )
    item_relation = ForeignKey(
        references=ItemRelation,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )


class UserContext(Table):
    id = UUID(primary_key=True)
    last_date = Timestamptz()
    is_active = Boolean(default=True)
    user = ForeignKey(
        references=Users,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
        )
    contex_1 = ForeignKey(
        references=Context,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )
    contex_2 = ForeignKey(
        references=Context,
        on_delete=OnDelete.restrict,
        on_update=OnUpdate.cascade
    )
