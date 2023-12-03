import dontmanage
from dontmanage.utils.caching import redis_cache
from pypika import Criterion

from helpdesk.utils import check_permissions


@dontmanage.whitelist()
@redis_cache()
def get_filterable_fields(doctype):
	check_permissions(doctype, None)
	QBDocField = dontmanage.qb.DocType("DocField")
	QBCustomField = dontmanage.qb.DocType("Custom Field")
	allowed_fieldtypes = [
		"Check",
		"Data",
		"Float",
		"Int",
		"Link",
		"Long Text",
		"Select",
		"Small Text",
		"Text Editor",
		"Text",
	]

	from_doc_fields = (
		dontmanage.qb.from_(QBDocField)
		.select(
			QBDocField.fieldname,
			QBDocField.fieldtype,
			QBDocField.label,
			QBDocField.name,
			QBDocField.options,
		)
		.where(QBDocField.parent == doctype)
		.where(QBDocField.hidden == False)
		.where(Criterion.any([QBDocField.fieldtype == i for i in allowed_fieldtypes]))
		.run(as_dict=True)
	)

	from_custom_fields = (
		dontmanage.qb.from_(QBCustomField)
		.select(
			QBCustomField.fieldname,
			QBCustomField.fieldtype,
			QBCustomField.label,
			QBCustomField.name,
			QBCustomField.options,
		)
		.where(QBCustomField.dt == doctype)
		.where(QBCustomField.hidden == False)
		.where(
			Criterion.any([QBCustomField.fieldtype == i for i in allowed_fieldtypes])
		)
		.run(as_dict=True)
	)

	res = []
	res.extend(from_doc_fields)
	res.extend(from_custom_fields)
	res.append(
		{
			"fieldname": "_assign",
			"fieldtype": "Link",
			"label": "Assigned to",
			"name": "_assign",
			"options": "HD Agent",
		}
	)
	return res
