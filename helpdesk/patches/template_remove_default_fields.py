import dontmanage
from dontmanage.query_builder import Case


def execute():
    QBDocField = dontmanage.qb.DocType("HD Ticket Template DocField")
    case = Case.any([QBDocField.fieldname == "Subject", QBDocField.fieldname == "Description"])
    dontmanage.qb.from_(QBDocField).delete().where(case).run()
    dontmanage.db.commit()
