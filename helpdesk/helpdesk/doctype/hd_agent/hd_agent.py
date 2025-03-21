# Copyright (c) 2022, DontManage Technologies and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class HDAgent(Document):
    def before_save(self):
        if self.name == self.user:
            return

        self.name = self.user
        self.set_user_roles()

    def set_user_roles(self):
        user = dontmanage.get_doc("User", self.user)
        for role in ["Agent"]:
            user.append("roles", {"role": role})
        user.save()

    @staticmethod
    def default_list_data():
        columns = [
            {
                "label": "Agent Name",
                "key": "agent_name",
                "width": "17rem",
                "type": "Data",
            },
            {
                "label": "Email",
                "key": "user.email as email",
                "width": "24rem",
                "type": "Data",
            },
            {
                "label": "Created On",
                "key": "creation",
                "width": "8rem",
                "type": "Datetime",
            },
        ]
        rows = ["modified", "user.user_image"]
        # modified row is needed because
        # we have a link table for HD Agent to User
        # and sql gets confused which modified to take from those 2 tables
        # hence throws ambiguous error
        return {"columns": columns, "rows": rows}


@dontmanage.whitelist()
def create_hd_agent(first_name, last_name, email, signature, team):
    if dontmanage.db.exists("User", email):
        user = dontmanage.get_doc("User", email)
    else:
        user = dontmanage.get_doc(
            {
                "doctype": "User",
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "email_signature": signature,
            }
        ).insert()

        user.send_welcome_mail_to_user()

    return dontmanage.get_doc(
        {"doctype": "HD Agent", "user": user.name, "group": team}
    ).insert()
