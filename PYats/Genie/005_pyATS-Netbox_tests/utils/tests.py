def verify_interface_enabled(netbox_interfaces, pyats_interfaces):
    """Verifies whether the current interface state matches what's in NetBox

    Args:
        netbox_interface: Interfaces for a given device in NetBox
        pyats_interfaces: Current interfaces on a device

    Returns:
        results: Dictionary containing list of passed interfaces, failed interfaces, and interfaces that need to be manually verified
    """

    results = {
        "PASS": [],
        "FAILED": [],
    }

    for interface in netbox_interfaces:
        if (interface.name in pyats_interfaces.keys()):
            if (interface.enabled):
                if (pyats_interfaces[interface.name]['enabled']):
                    if (pyats_interfaces[interface.name]['oper_status'] == "up"):
                        print(f"✅ {interface.name} FOUND in correct UP/UP state")
                        results['PASS'].append(interface)
                    else:
                        print(f"❌ {interface.name} FOUND in incorrect UP/DOWN state")
                        results['FAILED'].append(interface)
                elif (not pyats_interfaces[interface.name]['enabled']):
                    print(f"❌ {interface.name} FOUND in incorrect DOWN/DOWN state")
                    results['FAILED'].append(interface)
            elif (not interface.enabled):
                if (pyats_interfaces[interface.name]['enabled']):
                    if (pyats_interfaces[interface.name]['oper_status'] == "up"):
                        print(f"❌ {interface.name} FOUND in incorrect UP/UP state")
                        results['FAILED'].append(interface)
                    else:
                        print(f"❌ {interface.name} FOUND in incorrect UP/DOWN state")
                        results['FAILED'].append(interface)
                elif (not pyats_interfaces[interface.name]['enabled']):
                    print(f"✅ {interface.name} FOUND in correct DOWN/DOWN state")
                    results['PASS'].append(interface)
        else:
            print(f"❌ {interface.name} MISSING from device")
            results["FAIL"].append(interface)

    return results
