import dontmanage

no_cache = 1


def get_context(context):
	csrf_token = dontmanage.sessions.get_csrf_token()
	dontmanage.db.commit()
	context.csrf_token = csrf_token
