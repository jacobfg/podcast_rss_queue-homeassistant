"""The Podcast RSS to Queue integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_component import EntityComponent
import logging
import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import random

from .const import *

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Podcast RSS to Queue from a config entry."""
    # TODO Optionally store an object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = ...

    # TODO Optionally validate config entry options before setting up platform

    await hass.config_entries.async_forward_entry_setups(entry, (Platform.SENSOR,))

    # TODO Remove if the integration does not have an options flow
    entry.async_on_unload(entry.add_update_listener(config_entry_update_listener))

    return True


# TODO Remove if the integration does not have an options flow
async def config_entry_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener, called when the config entry options are changed."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry, (Platform.SENSOR,)
    ):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


def setup(hass, config):
    if DOMAIN not in config:
        return True
    return setup_entry(hass, config)

def setup_entry(hass, config_entry):
    EntityComponent(_LOGGER, DOMAIN, hass)

    def createqueue(call):
        data = call.data
        entity_id = data[CONF_ENTITY_ID]
        url = data[QUEUE_PODCAST_URL]
        randomise = data.get(QUEUE_RANDOM_ORDER, False)
        limit = data.get(QUEUE_LIMIT, 0)
        min_duration = data.get(QUEUE_MIN_DURATION, 0)
        
        episodes = get_episodes(url, limit=limit, min_duration=min_duration, randomise=randomise)

        hass.services.call('media_player', 'clear_playlist', {'entity_id': entity_id})

        for idx, episode in enumerate(episodes):
        # for episode in episodes:
            hass.services.call('media_player', 'play_media', {
                'entity_id': entity_id,
                'media_content_type': 'music',
                'media_content_id': episode['url'],
                'enqueue': 'play' if idx == 0 else 'add',
                'extra': {
                    'title': episode['title'],
                    'thumb': episode['image'],
                },
            })

            # logging.critical("Added to queue: " + episode['title'])
            # logging.critical("Added to queue: " + episode['url'])
            # logging.critical("Added to queue: " + episode['image'])

    def get_episodes(url, limit: int = 0, min_duration: int = 0, randomise: bool = False) -> list:
        # Create a handle, page, to handle the contents of the website
        page = requests.get(url)

        episodes = []

        soup = BeautifulSoup(page.content, features="xml")
        for episode in soup.select('item'):
            duration = int(episode.find("itunes:duration").text)
            if duration < min_duration: # skip short episodes
                continue
        
            title = episode.select('title')[0].text
                
            episodes.append({
                'title': EMOJI_PATTERN.sub(r'', title),
                'url':  episode.select('enclosure')[0]['url'].split('?')[0],
                'image': soup.channel.image.url.text.split('?')[0],
            })

        if randomise:
            random.shuffle(episodes)
        if limit > 0:
            return episodes[:limit]
        else:
            return episodes

    hass.services.register(DOMAIN, SERVICE_CREATE_QEUEUE, createqueue, SERVICE_CREATE_QEUEUE_SCHEMA)

    return True

    
