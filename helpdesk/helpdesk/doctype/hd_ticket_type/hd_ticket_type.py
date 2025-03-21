import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class HDTicketType(Document):
    def on_trash(self):
        self.prevent_system_delete()

    def prevent_system_delete(self):
        if self.is_system:
            dontmanage.throw(_("System types can not be deleted"))
