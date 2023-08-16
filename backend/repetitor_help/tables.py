from datetime import datetime

from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    UUID,
    Boolean,
    ForeignKey,
    Text,
    Timestamptz,
    Integer,
    OnDelete,
    OnUpdate,
)

from repetitor_backend.tables import Context


class Help(Table):
    """Describe help class."""

    id = UUID(primary_key=True)
    text = Text(null=False)
    language = ForeignKey(
        references=Context, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
    state = Varchar(null=True)
    total_impressions = Integer(default=0)
    positive_feedback = Integer(default=0)
    negative_feedback = Integer(default=0)
    auto_translation = Boolean()
    modified_on = Timestamptz(auto_update=datetime.utcnow())
    is_active = Boolean(default=True)

    context = ForeignKey(
        references=Context, on_delete=OnDelete.restrict, on_update=OnUpdate.cascade
    )
