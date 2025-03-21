# Copyright (c) 2024, DontManage Technologies and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class HDFormScript(Document):
    pass


def get_form_script(dt, apply_to="Form", is_customer_portal=False):
    """Returns the form script for the given doctype"""
    FormScript = dontmanage.qb.DocType("HD Form Script")
    query = (
        dontmanage.qb.from_(FormScript)
        .select("script")
        .where(FormScript.dt == dt)
        .where(FormScript.apply_to == apply_to)
        .where(FormScript.enabled == 1)
        .where(FormScript.apply_to_customer_portal == is_customer_portal)
    )

    doc = query.run(as_dict=True)
    if doc:
        return [d.script for d in doc] if len(doc) > 1 else doc[0].script
    else:
        return None
