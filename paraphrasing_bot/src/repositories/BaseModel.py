from sqlalchemy_mixins.repr import ReprMixin
from sqlalchemy_mixins.smartquery import SmartQueryMixin
from sqlalchemy_mixins.activerecord import ActiveRecordMixin

from paraphrasing_bot.app import db
from paraphrasing_bot.src.repositories.mixin.TimestampsMixin import TimestampsMixin
from paraphrasing_bot.src.repositories.mixin.SerializeMixin import SerializeMixin


class BaseModel(db.Model, ReprMixin, SmartQueryMixin, ActiveRecordMixin, TimestampsMixin, SerializeMixin):
    __abstract__ = True


BaseModel.set_session(db.session)
