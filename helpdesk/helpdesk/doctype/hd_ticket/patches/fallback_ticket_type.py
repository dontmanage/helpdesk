import dontmanage

from helpdesk.consts import DEFAULT_TICKET_TYPE


def execute():
    add_fallback()
    set_ticket_type()


def add_fallback():
    if dontmanage.db.exists("HD Ticket Type", DEFAULT_TICKET_TYPE):
        return
    d = dontmanage.new_doc("HD Ticket Type")
    d.is_system = True
    d.name = DEFAULT_TICKET_TYPE
    d.save()


def set_ticket_type():
    QBTicket = dontmanage.qb.DocType("HD Ticket")
    (
        dontmanage.qb.update(QBTicket)
        .set(QBTicket.ticket_type, DEFAULT_TICKET_TYPE)
        .where(QBTicket.ticket_type.isnull())
        .run()
    )
