"""The Flexit local integration."""
from __future__ import annotations

from homeassistant.const import Platform

# from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]


# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#    """Set up Flexit local from a config entry."""

#    hass.data.setdefault(DOMAIN, {})
# DO 1. Create API instance
# DO 2. Validate the API connection (and authentication)
# DO 3. Store an API object for your platforms to access
# hass.data[DOMAIN][entry.entry_id] = MyApi(...)

#    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

#    return True


# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#    """Unload a config entry."""
#    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
#        hass.data[DOMAIN].pop(entry.entry_id)

#    return unload_ok
