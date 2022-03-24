HOST_API = "https://logsight.ai/api/v1/"

PATH_USERS = "users"
PATH_USERS_DELETE = "users/{userId}"
PATH_LOGIN = "auth/login"

PATH_APP_CREATE = "users/{userId}/applications"
PATH_APP_LST = "users/{userId}/applications"
PATH_APP_DELETE = "users/{userId}/applications/{applicationId}"

PATH_LOGS = "logs"
PATH_LOGS_FILE = "logs/file?applicationId={applicationId}&tag={tag}"

PATH_LOGS_FLUSH = "logs/flush"
PATH_LOGS_INCIDENTS = "logs/incidents"

PATH_COMPARE = "logs/compare"
PATH_COMPARE_TAGS = "logs/compare/tags"
