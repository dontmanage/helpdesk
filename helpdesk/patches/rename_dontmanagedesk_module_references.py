import dontmanage

old_module = "DontManageDesk"
new_module = "Helpdesk"
doctypes = [
    "Report",
    "Server Script",
    "Web Form",
]


def execute():
    for doctype in doctypes:
        QBTable = dontmanage.qb.DocType(doctype)

        dontmanage.qb.update(QBTable).set(QBTable.module, new_module).where(
            QBTable.module == old_module
        ).run()
