import dontmanage


def on_assignment_rule_trash(doc, event):
    if not dontmanage.get_all(
        "Assignment Rule",
        filters={"document_type": "HD Ticket", "name": ["!=", doc.name]},
    ):
        dontmanage.throw("There should atleast be 1 assignment rule for ticket")
