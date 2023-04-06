# Copyright (c) 2022, DontManage Technologies and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class HDNotification(Document):
	def after_insert(self):
		dontmanage.publish_realtime("helpdesk:new-notification", user=self.to_user)
