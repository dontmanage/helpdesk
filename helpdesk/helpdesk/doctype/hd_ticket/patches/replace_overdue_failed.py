import dontmanage


def execute():
    QBTicket = dontmanage.qb.DocType("HD Ticket")
    dontmanage.qb.update(QBTicket).set(QBTicket.agreement_status, "Failed").where(
        QBTicket.agreement_status == "Overdue"
    ).run()
