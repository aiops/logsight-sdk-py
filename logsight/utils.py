import datetime
from dateutil.tz import tzlocal

from logsight.exceptions import LogsightException
from logsight.applications import LogsightApplication


def n_seconds_ago(seconds=60):
    return (datetime.datetime.now(tz=tzlocal()) - datetime.timedelta(seconds=seconds)).isoformat()


def now():
    return datetime.datetime.now(tz=tzlocal()).isoformat()


def create_apps(private_key, email, app_names):
    app_mng = LogsightApplication(private_key, email)
    return [create_app(app_mng, app_name) for app_name in app_names]


def delete_apps(private_key, email, app_names):
    app_mng = LogsightApplication(private_key, email)
    return [delete_app(app_mng, app_name) for app_name in app_names]


def create_app(app_mng, app_name):

    try:
        print('Creating app_name:', app_name)
        status_code, content = app_mng.create(app_name)
        if status_code != 200:
            raise LogsightException('Error creating app: %s' % app_name)
    except Exception:
        raise LogsightException('app_name already exists: %s' % app_name)

    return status_code, content


def delete_app(app_mng, app_name):

    status_code, content = app_mng.lst()
    app_list = [(d['id'], d['name']) for d in content if app_name in d['name']]

    if not app_list:
        raise LogsightException('Unable to delete app_name (it does not exist): %s' % app_name)

    app_id = app_list[0][0]
    try:
        print('Deleting app_name', app_name)
        status_code, content = app_mng.delete(app_id)
        if status_code != 200:
            raise LogsightException('Error deleting app: %s, %d' % (app_name, app_id))
    except Exception:
        raise LogsightException('app_name does not exists: %s, %d' % (app_name, app_id))

    return status_code, content
