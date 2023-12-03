import dontmanage


@dontmanage.whitelist()
def is_enabled():
    return bool(
        dontmanage.get_system_settings("enable_telemetry")
        and dontmanage.conf.get("posthog_host")
        and dontmanage.conf.get("posthog_project_id")
    )


@dontmanage.whitelist()
def get_credentials():
    return {
        "project_id": dontmanage.conf.get("posthog_project_id"),
        "telemetry_host": dontmanage.conf.get("posthog_host"),
    }
