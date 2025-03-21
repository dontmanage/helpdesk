import dontmanage
from dontmanage.permissions import add_permission


def execute():
    if dontmanage.db.exists("Role", "Agent"):
        add_permission("Communication", "Agent", 0)
