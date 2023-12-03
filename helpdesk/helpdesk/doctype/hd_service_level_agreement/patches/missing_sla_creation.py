import dontmanage


def execute():
	QBTicket = dontmanage.qb.DocType("HD Ticket")
	dontmanage.qb.update(QBTicket).set(
		QBTicket.service_level_agreement_creation, QBTicket.creation
	).where(QBTicket.service_level_agreement_creation.isnull()).run()
