# Copyright (c) 2023, DontManage Technologies and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document

from helpdesk.utils import capture_event, publish_event


class HDEscalationRule(Document):
    def validate(self):
        self.validate_criterion()
        self.validate_duplicate()

    def after_insert(self):
        self.emit_after_insert()

    def on_update(self):
        self.emit_on_update()

    def after_delete(self):
        self.emit_after_delete()

    def validate_criterion(self):
        if not (self.priority or self.team or self.ticket_type):
            dontmanage.throw(
                _("At-least one of priority, team and ticket type is required")
            )

    def validate_duplicate(self):
        is_duplicate = dontmanage.db.count(
            "HD Escalation Rule",
            filters={
                "name": ["!=", self.name],
                "priority": self.priority or "",
                "team": self.team or "",
                "ticket_type": self.ticket_type or "",
            },
        )

        if is_duplicate:
            dontmanage.throw(_("Escalation rule already exists for this criteria"))

    def emit_after_insert(self):
        capture_event("escalation_rule_created")
        publish_event("helpdesk:new-escalation-rule", self)

    def emit_on_update(self):
        capture_event("escalation_rule_updated")
        publish_event("helpdesk:update-escalation-rule", self)

    def emit_after_delete(self):
        capture_event("escalation_rule_deleted")
        publish_event("helpdesk:delete-escalation-rule", self)
