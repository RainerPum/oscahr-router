"""Collection of user prompts used by OSCAHR.

This module is part of the OSCAHR common package and contains a collection of user prompt functions
which multiple components of OSCAHR use.

Version: 0.6.1
Date: 13.07.2021
Author: Simon Birngruber (IoT-Lab, University of Applied Sciences Upper Austria, Campus Hagenberg)
License: MIT
"""

# Standard library imports
import logging

# Third party imports
import questionary

# Local application imports
import common.validation as validation

# Module variables
_log = logging.getLogger()  # get root logger


def prompt_device_name(registered_devices):
    """Prompts for a device name, validates it, checks for duplicates and prompts again if the
    name is already assigned.

    Args:
        registered_devices: A dictionary containing the registered devices.
    
    Returns:
        The chosen device name.
    """

    while True:
        device_name = questionary.text("Enter a name for the smart home device:",
                                       validate=validation.validate_device_name_text
                                       ).unsafe_ask().strip()

        if device_name in registered_devices.keys():
            _log.warning(f"Name '{device_name}' is already assigned, please choose another one!")
            continue
        else:
            break

    return device_name


def prompt_client_name(registered_devices, device_name=False):
    """Prompts for a client name and validates it. If a device name is given checks for
    duplicates and prompts again if the name is already assigned.

    Args:
        registered_devices: A dictionary containing the registered devices.
        device_name: Optional; Name of the device for which to search for duplicates. Default is
            False.

    Returns:
        The chosen client name.
    """

    while True:
        client_name = questionary.text(
            "Enter a name for the OSCAHR client to add:",
            validate=validation.validate_device_name_text).unsafe_ask().strip()

        if not device_name:
            break
        elif client_name in registered_devices[device_name]["clients"].keys():
            _log.warning(f"Name '{client_name}' is already assigned, please choose another one!")
            continue
        else:
            break

    return client_name


def prompt_ip_address(registered_devices=None, port=None):
    """Prompts for an IP address and validates it.
    If a registered_devices dictionary is given, checks for duplicates and prompts again if the IP
    address is already assigned to another registered device.
    If a registered_devices dictionary and a port is given checks for IP address/port combination
    duplicates prompts again if the IP address/port combination is already assigned to another
    registered device.

    Args:
        registered_devices: Optional; A dictionary containing the registered devices.
        port: Optional; An integer port number.
    
    Returns:
        The chosen IP address.
    """

    while True:
        ip_address = questionary.text("Enter the local IP address of the smart home device:",
                                      validate=validation.validate_ip_address_text).unsafe_ask()

        duplicate = False
        if registered_devices is not None:
            for name, value in registered_devices.items():
                if port is not None and value["ip_address"] == ip_address and \
                        value["port"] == port:
                    _log.warning("The same IP address and port combination is already assigned "
                                 f"for the device '{name}', please use the existing device "
                                 "instead or try again with another IP address!")
                    duplicate = True
                if port is None and value["ip_address"] == ip_address:
                    _log.warning("The same IP address is already assigned for the device "
                                 f"'{name}', please use the existing device instead or try again "
                                 "with another IP address!")
                    duplicate = True

        # Continue while loop if duplicate was found, otherwise end while loop
        if duplicate:
            continue
        else:
            break

    return ip_address


def prompt_onion_address(registered_devices):
    """Prompts for a address of a Tor Onion Service, validates it, checks for duplicates and 
    prompts again if the Onion address is already assigned to another registered device.

    Args:
        registered_devices: A dictionary containing the registered devices.

    Returns:
        The chosen Tor Onion address.
    """

    while True:
        onion_address = questionary.text(
            "Enter the Tor Onion address generated by the OSCAHR Proxy:",
            validate=validation.validate_onion_v3_address_text).unsafe_ask()

        # Tor Browser doesn't support two client authorization files with the same
        # Onion address, therefore check if a device with the given Onion address exists
        duplicate = False
        for device in registered_devices.keys():
            if onion_address == registered_devices[device]["onion_address"]:
                _log.warning(f"Onion address '{onion_address}' is already registered for device "
                             f"'{device}', please use the existing device instead or try again "
                             "with another Onion address!")
                duplicate = True

        # Continue while loop if duplicate was found, otherwise end while loop
        if duplicate:
            continue
        else:
            break

    return onion_address


def prompt_port(registered_devices=None, ip_address=None):
    """Prompts for a webinterface port and validates it.
    If a registered_devices dictionary and an IP address is given checks for IP address/port
    combination duplicates and prompts again if the IP address/port combination is already
    assigned to another registered device.

    Args:
        registered_devices: Optional; A dictionary containing the registered devices.
        ip_address: Optional; An IP address as string.

    Returns:
        The chosen port number.
    """

    while True:
        port = int(questionary.text("Enter the port of the smart home device webinterface:",
                                    validate=validation.validate_port_text).unsafe_ask())

        duplicate = False
        if registered_devices is not None and ip_address is not None:
            for name, value in registered_devices.items():
                if value["ip_address"] == ip_address and value["port"] == port:
                    _log.warning("The same IP address and port combination is already assigned "
                                 f"for the device '{name}', please use the existing device "
                                 "instead or try again with another webinterface port!")
                    duplicate = True

        # Continue while loop if duplicate was found, otherwise end while loop
        if duplicate:
            continue
        else:
            break

    return port


def prompt_public_key():
    """Prompts for the public key and validates it.

    Returns:
        The chosen public key.
    """

    return questionary.text("Enter the public key generated by the OSCAHR client:",
                            validate=validation.validate_base32_key_text).unsafe_ask()


def prompt_https():
    """Prompts for the usage of HTTPS.
    
    Returns:
        True if HTTPS should be used, False if not.
    """

    https = questionary.confirm("Would you like to use HTTPS for the connection to your smart "
                                "home device?").unsafe_ask()

    if https:
        _log.info("A certificate warning will occur when accessing the smart home device "
                  "webinterface because the address of the Tor Onion Service is not stored in the "
                  "certificate.")
    else:
        _log.warning("WARNING: The connection between the OSCAHR Proxy and the smart home device "
                     "is NOT protected by OSCAHR!")

    return https
