import dontmanage
from dontmanage.utils import get_table_name

from helpdesk.utils import alphanumeric_to_int

DOCTYPES = [
    "HD Preset Filter Item",
    "HD Team Item",
    "HD Team Member",
    "HD Ticket",
    "HD Ticket Custom Field Item",
]
MODULE = "Helpdesk"
SEQ_SUFFIX = "_id_seq"


def execute():
    modify_table()
    create_sequence()


def modify_table():
    for doctype in DOCTYPES:
        table = f"`{get_table_name(doctype)}`"
        dontmanage.db.sql_ddl(f"ALTER TABLE {table} MODIFY COLUMN name BIGINT(20)")
        dontmanage.reload_doc(MODULE, "DocType", doctype)


def create_sequence():
    for doctype in DOCTYPES:
        sequence_name = dontmanage.scrub(doctype + SEQ_SUFFIX)
        dontmanage.db.sql_ddl(f"DROP SEQUENCE IF EXISTS {sequence_name}")
        start_value = sequence_start(doctype)
        dontmanage.db.create_sequence(
            doctype, check_not_exists=False, start_value=start_value
        )


def sequence_start(doctype: str):
    try:
        last_doc = dontmanage.get_last_doc(doctype, order_by="name desc")
        last_id = last_doc.name

        if isinstance(last_id, int):
            return last_id

        last_id = alphanumeric_to_int(last_id) or 0
        return last_id + 1
    except Exception:
        return 1
