"""Data update coordinator for the Radarr integration."""
from __future__ import annotations

from abc import abstractmethod
from datetime import timedelta
from typing import Generic, TypeVar, cast

from aiopyarr import RootFolder, exceptions
from aiopyarr.models.host_configuration import PyArrHostConfiguration
from aiopyarr.radarr_client import RadarrClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER

T = TypeVar("T", str, list[RootFolder], int)


class RadarrDataUpdateCoordinator(DataUpdateCoordinator, Generic[T]):
    """Data update coordinator for the Radarr integration."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        host_configuration: PyArrHostConfiguration,
        api_client: RadarrClient,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.api_client = api_client
        self.host_configuration = host_configuration
        self.system_version: str | None = None

    async def _async_update_data(self) -> T:
        """Get the latest data from Radarr."""
        try:
            return await self._fetch_data()

        except exceptions.ArrConnectionException as ex:
            raise UpdateFailed(ex) from ex
        except exceptions.ArrAuthenticationException as ex:
            raise ConfigEntryAuthFailed(
                "API Key is no longer valid. Please reauthenticate"
            ) from ex

    @abstractmethod
    async def _fetch_data(self) -> T:
        """Fetch the actual data."""
        raise NotImplementedError


class StatusDataUpdateCoordinator(RadarrDataUpdateCoordinator):
    """Status update coordinator for Radarr."""

    async def _fetch_data(self) -> str:
        """Fetch the data."""
        return (await self.api_client.async_get_system_status()).version


class DiskSpaceDataUpdateCoordinator(RadarrDataUpdateCoordinator):
    """Disk space update coordinator for Radarr."""

    async def _fetch_data(self) -> list[RootFolder]:
        """Fetch the data."""
        return cast(list, await self.api_client.async_get_root_folders())


class MoviesDataUpdateCoordinator(RadarrDataUpdateCoordinator):
    """Movies update coordinator."""

    async def _fetch_data(self) -> int:
        """Fetch the movies data."""
        return len(cast(list, await self.api_client.async_get_movies()))
