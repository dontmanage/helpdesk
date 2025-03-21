import dontmanage
from dontmanage.utils.telemetry import POSTHOG_HOST_FIELD, POSTHOG_PROJECT_FIELD


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


@dontmanage.whitelist()
def get_posthog_settings():
    return {
        "posthog_project_id": dontmanage.conf.get(POSTHOG_PROJECT_FIELD),
        "posthog_host": dontmanage.conf.get(POSTHOG_HOST_FIELD),
        "enable_telemetry": dontmanage.get_system_settings("enable_telemetry"),
        "telemetry_site_age": dontmanage.utils.telemetry.site_age(),
    }
