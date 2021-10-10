import datetime
from dateutil.tz import tzlocal

from logsight.exceptions import LogsightException
from logsight.application.application import LogsightApplication


def n_seconds_ago(seconds=60):
    now = datetime.datetime.now(tz=tzlocal())
    return (now - datetime.timedelta(seconds=seconds)).isoformat()


def now():
    return datetime.datetime.now(tz=tzlocal()).isoformat()


def create_apps(private_key, email, app_names):
    app_mng = LogsightApplication(private_key, email)
    return [app_mng.create(app_name) for app_name in app_names]


def delete_apps(private_key, email, app_names):
    app_mng = LogsightApplication(private_key, email)
    return [delete_app(app_mng, app_name) for app_name in app_names]


def delete_app(app_mng, app_name):

    content = app_mng.lst()
    app_list = [(d["id"], d["name"]) for d in content if app_name in d["name"]]

    if not app_list:
        raise LogsightException(
            "Unable to delete app_name (it does not exist): %s" % app_name
        )

    app_id = app_list[0][0]
    try:
        print("Deleting app_name", app_name)
        content = app_mng.delete(app_id)
    except LogsightException:
        print("app_name does not exists: %s, %d" % (app_name, app_id))

    return content
