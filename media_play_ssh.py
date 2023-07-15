from homeassistant.components import media_source
from homeassistant.components.media_player.browse_media import (
    async_process_play_media_url,
)
import asyncio

@service
def media_play_ssh(host=None, media_content_id=None, entity_id=None):
    play_ssh(host, media_content_id, entity_id)

async def play_ssh(host, media_id, entity_id):
    if media_source.is_media_source_id(media_id):
        play_item = media_source.async_resolve_media(hass, media_id, entity_id)

        media_id = async_process_play_media_url(hass, play_item.url)

        await asyncio.create_subprocess_shell(
            f"ffmpeg -i {media_id} -c:a libvorbis -f ogg - | ssh {host} ogg123 -"
        )
    else:
        log.info(
            "Invalid media type"
        )
