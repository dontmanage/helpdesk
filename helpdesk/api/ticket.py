import dontmanage


def assign_ticket_to_agent(ticket_id, agent_id=None):
    if not ticket_id:
        return

    ticket_doc = dontmanage.get_doc("HD Ticket", ticket_id)

    if not agent_id:
        # assign to self
        agent_id = dontmanage.session.user

    if not dontmanage.db.exists("HD Agent", agent_id):
        dontmanage.throw("Tickets can only assigned to agents")

    ticket_doc.assign_agent(agent_id)
    return ticket_doc


@dontmanage.whitelist()
def bulk_assign_ticket_to_agent(ticket_ids, agent_id=None):
    if ticket_ids:
        ticket_docs = []
        for ticket_id in ticket_ids:
            ticket_doc = assign_ticket_to_agent(ticket_id, agent_id)
            ticket_docs.append(ticket_doc)
        return ticket_docs
