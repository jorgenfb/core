"""Constants for the Flexit local integration."""

DOMAIN = "flexit_local"


SENSOR_MAPPING = {
    # Outside air temperature
    "analogInput:1": {"name": "Intake air temperature"},
    # Supply air temperature
    "analogInput:4": {"name": "Supply air temperature"},
    # Extract air temperature
    "analogInput:59": {"name": "Extract air temperature"},
    # Exhaust air temperature
    "analogInput:11": {"name": "Exhaust air temperature"},
    # Room temperature
    "analogInput:75": {"name": "Room temperature"},
    # "multiStateValue:42",  # Present ventilation mode
}
