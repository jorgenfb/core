"""Platform for sensor integration."""
from __future__ import annotations

import BAC0

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

# from .const import SENSOR_MAPPING


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""

    bacnet = BAC0.lite()

    add_entities(
        [
            AnalogInputSensor(bacnet, index=1, name="Intake air temperature"),
            AnalogInputSensor(bacnet, index=4, name="Supply air temperature"),
            AnalogInputSensor(bacnet, index=11, name="Exhaust air temperature"),
            AnalogInputSensor(bacnet, index=59, name="Extract air temperature"),
        ]
    )


class AnalogInputSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Intake air temperature"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, bacnet, index, name):
        """Initialize an analog sensor."""
        self._bacnet = bacnet
        self._index = index
        self._attr_name = name

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        name = "analogInput:1"

        objects = {}
        objects[name] = ["presentValue"]

        req = {"address": "192.168.1.47", "objects": objects}

        result = self._bacnet.readMultiple("192.168.1.47", request_dict=req)

        measurement = result[("analogInput", 1)][0][1]

        self._attr_native_value = measurement
