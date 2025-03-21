import dontmanage

from helpdesk.consts import DEFAULT_TICKET_TEMPLATE


def create_default_template():
    if dontmanage.db.exists("HD Ticket Template", DEFAULT_TICKET_TEMPLATE):
        return
    doc = {
        "doctype": "HD Ticket Template",
        "template_name": DEFAULT_TICKET_TEMPLATE,
    }
    dontmanage.get_doc(doc).save()
