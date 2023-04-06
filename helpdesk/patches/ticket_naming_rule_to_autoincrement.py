import dontmanage
from dontmanage.utils import get_table_name

from helpdesk.utils import alphanumeric_to_int

DOCTYPE = "HD Ticket"
MODULE = "Helpdesk"
SEQ_SUFFIX = "_id_seq"


def execute():
	create_sequence()
	modify_table()


def modify_table():
	table = f"`{get_table_name(DOCTYPE)}`"
	dontmanage.db.sql_ddl(f"ALTER TABLE {table} MODIFY COLUMN name BIGINT(20)")
	dontmanage.reload_doc(MODULE, "DocType", DOCTYPE)


def create_sequence():
	sequence_name = dontmanage.scrub(DOCTYPE + SEQ_SUFFIX)
	dontmanage.db.sql_ddl(f"DROP SEQUENCE IF EXISTS {sequence_name}")
	start_value = sequence_start()
	dontmanage.db.create_sequence(DOCTYPE, check_not_exists=False, start_value=start_value)


def sequence_start():
	try:
		last_doc = dontmanage.get_last_doc(DOCTYPE)
		last_id = alphanumeric_to_int(last_doc.name) or 0
		return last_id + 1
	except:
		return 1
