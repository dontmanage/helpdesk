import dontmanage
from dontmanage.model.document import Document
from dontmanage.query_builder import JoinType
from dontmanage.utils import now_datetime
from pypika import Criterion

from helpdesk.utils import check_permissions, get_context

DOCTYPE = "HD Service Level Agreement"


def get_sla(ticket: Document) -> Document:
	"""
	Get Service Level Agreement for `ticket`

	:param doc: Ticket to use
	:return: Applicable SLA
	"""
	check_permissions(DOCTYPE, None)
	QBSla = dontmanage.qb.DocType(DOCTYPE)
	QBPriority = dontmanage.qb.DocType("HD Service Level Priority")
	now = now_datetime()
	priority = ticket.priority
	q = (
		dontmanage.qb.from_(QBSla)
		.select(QBSla.name, QBSla.condition)
		.where(QBSla.enabled == True)
		.where(QBSla.default_sla == False)
		.where(Criterion.any([QBSla.start_date.isnull(), QBSla.start_date <= now]))
		.where(Criterion.any([QBSla.end_date.isnull(), QBSla.end_date >= now]))
	)
	if priority:
		q = (
			q.join(QBPriority, JoinType.inner)
			.on(QBPriority.parent == QBSla.name)
			.where(QBPriority.priority == priority)
		)
	sla_list = q.run(as_dict=True)
	res = None
	for sla in sla_list:
		cond = sla.get("condition")
		if not cond or dontmanage.safe_eval(cond, None, get_context(ticket)):
			res = sla
			break
	return res or get_default()


def get_default() -> Document:
	"""
	Get default Service Level Agreement

	:return: Default SLA
	"""
	return dontmanage.get_last_doc(
		DOCTYPE,
		filters={
			"enabled": True,
			"default_sla": True,
		},
	)
