# Copyright (c) 2022, DontManage Technologies and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class HDPresetFilter(Document):
    def before_save(self):
        if self.type == "User":
            self.user = dontmanage.session.user

    def on_trash(self):
        if self.type == "System":
            dontmanage.throw("System filters cannot be deleted")

    def after_insert(self):
        dontmanage.publish_realtime("helpdesk:new-preset-filter", self)
