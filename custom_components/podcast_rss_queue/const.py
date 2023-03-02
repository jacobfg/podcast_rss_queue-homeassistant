"""Constants for the Podcast RSS to Queue integration."""

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_ENTITY_ID, CONF_NAME

import voluptuous as vol
import re

DOMAIN = "podcast_rss_queue"

QUEUE_RANDOM_ORDER = 'randomise'
QUEUE_LIMIT = 'limit'
QUEUE_PODCAST_URL = 'url'
QUEUE_MIN_DURATION = 'min_duration'

EMOJI_PATTERN = re.compile("["
    u"\U0001F600-\U0001F64F" # emoticons
    u"\U0001F300-\U0001F5FF" # symbols & pictographs
    u"\U0001F680-\U0001F6FF" # transport & map symbols
    u"\U0001F1E0-\U0001F1FF" # flags (iOS)
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u'\U00010000-\U0010ffff'
    u"\u200d"
    u"\u2640-\u2642"
    u"\u2600-\u2B55"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\u3030"
    u"\ufe0f"
    u"\u2069"
    u"\u2066"
    u"\u200c"
    u"\u2068"
    u"\u2067"
    "]+", flags=re.UNICODE)

SERVICE_CREATE_QEUEUE = 'create_queue'
SERVICE_CREATE_QEUEUE_SCHEMA = vol.Schema({
    vol.Required(CONF_ENTITY_ID): cv.entity_id,
    vol.Required(QUEUE_PODCAST_URL): cv.url,
    vol.Optional(QUEUE_LIMIT): int,
    vol.Optional(QUEUE_MIN_DURATION): int,
    vol.Optional(QUEUE_RANDOM_ORDER): cv.boolean,
})
