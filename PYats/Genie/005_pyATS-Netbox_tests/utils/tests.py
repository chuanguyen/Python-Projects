def verify_interface_enabled(netbox_interfaces, pyats_interfaces):
    """Verifies whether the current interface state matches what's in NetBox

    Args:
        netbox_interface: Interfaces for a given device in NetBox
        pyats_interfaces: Current interfaces on a device

    Returns:
        results: Dictionary containing list of passed interfaces and failed interfaces
    """

    results = {
        "PASS": [],
        "FAILED": [],
    }

    for interface in netbox_interfaces:
        interface_exists = interface.name in pyats_interfaces.keys()
        pyats_interface_enabled = pyats_interfaces[interface.name]['enabled']
        pyats_interface_oper_status = pyats_interfaces[interface.name]['oper_status']

        if (interface_exists):
            if (interface.enabled):
                if (pyats_interface_enabled):
                    if (pyats_interface_oper_status == "up"):
                        print(f"✅ {interface.name} found in correct UP/UP state")
                        results['PASS'].append(interface)
                    else:
                        print(f"❌ {interface.name} found in incorrect UP/DOWN state")
                        results['FAILED'].append(interface)
                elif (not pyats_interfaces[interface.name]['enabled']):
                    print(f"❌ {interface.name} found in incorrect DOWN/DOWN state")
                    results['FAILED'].append(interface)
            elif (not interface.enabled):
                if (pyats_interface_enabled):
                    if (pyats_interface_oper_status == "up"):
                        print(f"❌ {interface.name} found in incorrect UP/UP state")
                        results['FAILED'].append(interface)
                    else:
                        print(f"❌ {interface.name} found in incorrect UP/DOWN state")
                        results['FAILED'].append(interface)
                elif (not pyats_interfaces[interface.name]['enabled']):
                    print(f"✅ {interface.name} found in correct DOWN/DOWN state")
                    results['PASS'].append(interface)
        else:
            print(f"❌ {interface.name} MISSING from device")
            results["FAILED"].append(interface)

    return results

def verify_interface_description(netbox_interfaces, pyats_interfaces):
        """Verifies whether the current interface description matches what's in NetBox

        Args:
            netbox_interface: Interfaces for a given device in NetBox
            pyats_interfaces: Current interfaces on a device

        Returns:
            results: Dictionary containing list of passed interfaces and failed interfaces
        """

        results = {
            "PASS": [],
            "FAILED": [],
        }

        for interface in netbox_interfaces:
            interface_exists = interface.name in pyats_interfaces.keys()
            interface_description_exists = len(interface.description) > 0

            if (interface_exists):
                if (interface_description_exists):
                    if ('description' in pyats_interfaces[interface.name].keys()):
                        if (pyats_interfaces[interface.name]['description'] == interface.description):
                            print(f"✅ {interface.name} description is CORRECT")
                            results['PASS'].append(interface)
                        elif (not pyats_interfaces[interface.name]['description'] == interface.description):
                            print(f"❌ {interface.name} description is INCORRECT and should be '{interface.description}'")
                            results["FAILED"].append(interface)
                    else:
                        print(f"❌ {interface.name} has NO description set. Should be '{interface.description}'")
                        results["FAILED"].append(interface)
                else:
                    if ('description' not in pyats_interfaces[interface.name].keys()):
                        print(f"✅ {interface.name} has NO description set")
                        results['PASS'].append(interface)
                    else:
                        print(f"""❌ {interface.name} incorrectly has description '{pyats_interfaces[interface.name]['description']}' on switch""")
                        results["FAILED"].append(interface)
            else:
                print(f"❌ {interface.name} MISSING from device")
                results["FAILED"].append(interface)

        return results
