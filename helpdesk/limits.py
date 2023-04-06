import dontmanage
from dontmanage import _


class PaywallReachedError(dontmanage.ValidationError):
	pass


def validate_agent_count(doc, method):
	plan = dontmanage.conf.plan
	count = dontmanage.db.count("HD Agent")

	if plan == "Starter" and count >= 3:
		dontmanage.throw(
			_("Only a maximum of 3 agents are allowed as per your plan"), exc=PaywallReachedError
		)
	elif plan == "Essential" and count >= 10:
		dontmanage.throw(
			_("Only a maximum of 10 agents are allowed as per your plan"),
			exc=PaywallReachedError,
		)
	elif plan == "Custom":
		# TODO: add custom plans here via some api or something.
		pass
