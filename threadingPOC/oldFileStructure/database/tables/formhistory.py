from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

__version__ = '0.1.0'

# browser time format
DT_MILLI_ZEROED_MICRO = "datetime_milliseconds_zeroed_microseconds"
# objects
Base = declarative_base()


class FormHistory(Base):
    ID = "ID"
    FIELD_NAME = "Feldname"
    VALUE = "Eingabewert"
    FIRST_USED = "Zum ersten mal verwendet"
    LAST_USED = "Zuletzt genutzt"

    __tablename__ = 'moz_formhistory'  # HISTORY

    id = Column("id", Integer, primary_key=True)
    field_name = Column("fieldname", String)
    value = Column("value", String)
    first_used_timestamp = Column("firstUsed", Integer)
    last_used_timestamp = Column("lastUsed", Integer)

    # @orm.reconstructor - throws error, not knowing orm name
    def __init__(self):
        self.attr_list = []
        self.attr_list.append(BaseAttribute(FIELD_NAME, OTHER, self.field_name))
        self.attr_list.append(BaseAttribute(VALUE, OTHER, self.value))
        self.attr_list.append(BaseAttribute(FIRST_USED, DT_MILLI_ZEROED_MICRO, self.first_used_timestamp))
        self.attr_list.append(BaseAttribute(LAST_USED, DT_MILLI_ZEROED_MICRO, self.last_used_timestamp))

    def __repr__(self):
        return "<FormHistory(field_name='%s', value='%s', first_used_timestamp='%d', last_used_timestamp='%d')>" % (
            self.field_name, self.value, self.first_used_timestamp, self.last_used_timestamp)

    def count_rows(self, dbms):
        count_q = dbms.statement.with_only_columns([func.count()]).order_by(None)
        counted = dbms.session.execute(count_q).scalar()
        return counted
