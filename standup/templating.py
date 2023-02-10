import jinja2

from .filters import emojify
from .filters import ensure_list
from .filters import slack_bold

_STANDUP_TEMPLATE_FILE = "standup.slack.j2"
_CONFIG_TEMPLATE_FILE = "config.ini.j2"

_TEMPLATE_LOADER = jinja2.PackageLoader(package_name="standup")
_TEMPLATE_ENV = jinja2.Environment(loader=_TEMPLATE_LOADER)
_TEMPLATE_ENV.filters.update(
    {
        "emojify": emojify,
        "slack_bold": slack_bold,
        "ensure_list": ensure_list,
    },
)

STANDUP_TEMPLATE = _TEMPLATE_ENV.get_template(_STANDUP_TEMPLATE_FILE)
CONFIG_TEMPLATE = _TEMPLATE_ENV.get_template(_CONFIG_TEMPLATE_FILE)
