from typing import Literal

import dontmanage

# from dontmanage import _
from pypika import JoinType

from helpdesk.utils import check_permissions

DOCTYPE_TEMPLATE = "HD Ticket Template"
DOCTYPE_TEMPLATE_FIELD = "HD Ticket Template Field"
DOCTYPE_TICKET = "HD Ticket"


@dontmanage.whitelist()
def get_one(name: str):
    check_permissions(DOCTYPE_TEMPLATE, None)
    found, about = dontmanage.get_value(DOCTYPE_TEMPLATE, name, ["name", "about"]) or [
        None,
        None,
    ]
    if not found:
        return {"about": None, "fields": []}

    fields = []
    fields.extend(get_fields(name, "DocField"))
    fields.extend(get_fields(name, "Custom Field"))
    return {
        "about": about,
        "fields": fields,
    }


def get_fields(template: str, fetch: Literal["Custom Field", "DocField"]):
    QBField = dontmanage.qb.DocType(DOCTYPE_TEMPLATE_FIELD)
    QBFetch = dontmanage.qb.DocType(fetch)
    fields = (
        dontmanage.qb.from_(QBField)
        .select(QBField.star)
        .where(QBField.parent == template)
        .where(QBField.parentfield == "fields")
        .where(QBField.parenttype == DOCTYPE_TEMPLATE)
    )
    where_parent = QBFetch.parent == DOCTYPE_TICKET
    if fetch == "Custom Field":
        where_parent = QBFetch.dt == DOCTYPE_TICKET
    return (
        dontmanage.qb.from_(fields)
        .select(
            QBFetch.description,
            QBFetch.fieldtype,
            QBFetch.label,
            QBFetch.options,
            fields.fieldname,
            fields.hide_from_customer,
            fields.required,
            fields.url_method,
            fields.placeholder,
        )
        .join(QBFetch, JoinType.inner)
        .on(QBFetch.fieldname == fields.fieldname)
        .where(where_parent)
        .orderby(fields.idx)
        .run(as_dict=True)
    )
