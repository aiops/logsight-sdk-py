import os

HOST_API = "https://logsight.ai/api/v1/"


def set_host(url):
    global HOST_API
    HOST_API = url


def get_tags_from_env():
    tags = {}
    tag_prefix = "LOGSIGHT_TAG"
    for k, v in os.environ.items():
        if tag_prefix == k[:len(tag_prefix)]:
            tag_name = k.split(tag_prefix)[1].lower().lstrip("_")
            tags[tag_name] = v
    return tags
