import dontmanage

from helpdesk import __version__

no_cache = 1


def get_context(context):
	context.csrf_token = dontmanage.sessions.get_csrf_token()
	context.dontmanage_version = dontmanage.__version__
	context.helpdesk_version = __version__
	context.site_name = dontmanage.local.site
	dontmanage.db.commit()
