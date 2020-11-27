#!/usr/bin/env python

def create_nb_obj_dict(nb, required_non_id, required_id, optional_non_id, optional_id):
    """Accepts attributes for NetBox model and will create a dict that can be used for object creation

    Args:
        nb: PyNetbox connection to a Netbox instance
        required_non_id: NB Model attributes that don't require NB IDs
        required_id: NB Model attributes that only accept NB IDs
        optional_non_id: NB Model attributes that don't require NB IDs
        optional_id: NB Model attributes that only accept NB IDs

    Returns:
        nb_obj_dict: Dictionary containing all the required and any optional fields for NetBox object creation

    """
    nb_obj_dict = dict()

    if (required_non_id):
        for attr_key,attr_value in required_non_id.items():
            nb_obj_dict[attr_key] = attr_value

    if (required_id):
        for attr_key,attr_values in required_id.items():
            nb_obj_dict[attr_key] = retrieve_nb_id(nb, attr_values['app'], attr_values['model'], attr_values['name'])

    if (optional_non_id):
        for attr_key,attr_value in optional_non_id.items():
            if (attr_value):
                nb_obj_dict[attr_key] = attr_value

    if (optional_id):
        for attr_key,attr_values in optional_id.items():
            if (attr_values):
                nb_obj_dict[attr_key] = retrieve_nb_id(nb, attr_values['app'], attr_values['model'], attr_values['name'])

    return nb_obj_dict

def create_nb_obj(nb, nb_app, model, nb_obj_dict):
    """Accepts dictionary of NetBox model attributes and will create the NetBox object

    Args:
        nb: PyNetbox connection to a Netbox instance
        nb_app: String of NetBox app type
        model: String of NetBox model type
        nb_obj_dict: Dictionary of NetBox model attributes
    """

    if (nb_app == "dcim"):
        if (model == "regions"):
            nb.dcim.regions.create(nb_obj_dict)
        elif (model == "sites"):
            nb.dcim.sites.create(nb_obj_dict)
        elif (model == "rack_roles"):
            nb.dcim.rack_roles.create(nb_obj_dict)
        elif (model == "rack_groups"):
            nb.dcim.rack_groups.create(nb_obj_dict)
        elif (model == "racks"):
            nb.dcim.racks.create(nb_obj_dict)
        elif (model == "device_roles"):
            nb.dcim.device_roles.create(nb_obj_dict)
        elif (model == "manufacturers"):
            nb.dcim.manufacturers.create(nb_obj_dict)
        elif (model == "platforms"):
            nb.dcim.platforms.create(nb_obj_dict)

    if (nb_app == "ipam"):
        if (model == "rirs"):
            nb.ipam.rirs.create(nb_obj_dict)
        elif (model == "aggregates"):
            nb.ipam.aggregates.create(nb_obj_dict)
        elif (model == "roles"):
            nb.ipam.roles.create(nb_obj_dict)
        elif (model == "vlan_groups"):
            nb.ipam.vlan_groups.create(nb_obj_dict)
        elif (model == "vlans"):
            nb.ipam.vlans.create(nb_obj_dict)
        elif (model == "vrfs"):
            nb.ipam.vrfs.create(nb_obj_dict)
        elif (model == "prefixes"):
            nb.ipam.prefixes.create(nb_obj_dict)

def retrieve_nb_obj(nb, app, model, searchTerm):
    """Searches for a NetBox object of a given model based on a search term and returns the object

      Args:
        nb: PyNetbox connection to a Netbox instance
        app: NetBox app being searched
        model: NetBox model to look for
        searchTerm: Query term used to locate given NetBox object

      Returns:
        If found: Returns discovered NetBox object
        If not found: Returns None
    """

    nb_obj = None
    searchTerm_modified = None

    # Alters search term to match the slug formatting (lowercase and dashes)
    if (type(searchTerm) is str):
        searchTerm_modified = searchTerm.lower().replace(" ", "-")
    else:
        searchTerm_modified = searchTerm

    if (app == "dcim"):
        if (model == "regions"):
            nb_obj = nb.dcim.regions.get(slug=searchTerm_modified)
        elif (model == "sites"):
            nb_obj = nb.dcim.sites.get(slug=searchTerm_modified)
        elif (model == "rack_roles"):
            nb_obj = nb.dcim.rack_roles.get(slug=searchTerm_modified)
        elif (model == "rack_groups"):
            nb_obj = nb.dcim.rack_groups.get(slug=searchTerm_modified)
        elif (model == "racks"):
            nb_obj = nb.dcim.racks.get(name=searchTerm_modified)
        elif (model == "devices"):
            nb_obj = nb.dcim.devices.get(name=searchTerm)
        elif (model == "device_roles"):
            nb_obj = nb.dcim.device_roles.get(slug=searchTerm_modified)
        elif (model == "device_types"):
            nb_obj = nb.dcim.device_types.get(slug=searchTerm_modified)
        elif (model == "manufacturers"):
            nb_obj = nb.dcim.manufacturers.get(slug=searchTerm_modified)
        elif (model == "platforms"):
            nb_obj = nb.dcim.platforms.get(slug=searchTerm_modified)
    elif (app == "ipam"):
        if (model == "rirs"):
            nb_obj = nb.ipam.rirs.get(slug=searchTerm_modified)
        elif (model == "aggregates"):
            nb_obj = nb.ipam.aggregates.get(prefix=searchTerm_modified)
        elif (model == "roles"):
            nb_obj = nb.ipam.roles.get(slug=searchTerm_modified)
        elif (model == "prefixes"):
            nb_obj = nb.ipam.prefixes.get(prefix=searchTerm_modified)
        elif (model == "vlan_groups"):
            nb_obj = nb.ipam.vlan_groups.get(slug=searchTerm_modified)
        elif (model == "vlans"):
            nb_obj = nb.ipam.vlans.get(vid=searchTerm_modified)
        elif (model == "vrfs"):
            nb_obj = nb.ipam.vrfs.get(name=searchTerm_modified)

    return nb_obj

def retrieve_nb_identifier(model):
    """Provides the unique search value for a given NetBox model

      Returns:
        String of search value
    """
    # Returns human-friendly identifier for the given NetBox model

    # Stores the corresponding identifying field for the given NetBox objct
    nb_obj_name_keys = dict(
        regions="slug",
        sites="slug",
        rack_groups="slug",
        rack_roles="slug",
        racks="name",
        devices="name",
        device_roles="slug",
        device_type="slug",
        manufacturers="slug",
        platforms="slug",
        rirs="slug",
        aggregates="prefix",
        roles="slug",
        prefixes="prefix",
        vlan_groups="slug",
        vlans="vid",
        vrfs="name"
    )

    return nb_obj_name_keys[model]

def retrieve_nb_id(nb, app, model, searchTerm):
    """Searches for a NetBox object of a given model based on a search term and returns the ID

      Args:
        nb: PyNetbox connection to a Netbox instance
        app: NetBox app being searched
        model: NetBox model to look for
        searchTerm: Query term used to locate given NetBox object

      Returns:
        If found: Returns integer ID of discovered NetBox object
        If not found: Returns the original search term
    """
    # Searches for a NetBox object of a given model based on a search term and returns the ID
    # If object can't be found, returns the search term
    nb_obj_id = None
    nb_obj = None

    nb_obj=retrieve_nb_obj(nb, app,model,searchTerm)

    if (nb_obj):
        nb_obj_id = nb_obj.id
        return nb_obj_id
    else:
        return searchTerm

def retrieve_termination_obj(nb,termination_type,dev_name,termination_name):
    """Searches for a NetBox termination object of a given name from a given device

      Args:
        nb: PyNetbox connection to a Netbox instance
        termination_type: NetBox termination object type (ie. dcim.interface)
        dev_name: Name of NetBox device being searched
        termination_name: Name of NetBox termination object being searched

      Returns:
        If found: Returns NetBox termination object
        If not found: Returns None
    """

    termination_obj = None

    if (termination_type == "dcim.interface"):
        termination_obj = nb.dcim.interfaces.get(device=dev_name,name=termination_name)
    elif (termination_type == "dcim.frontport"):
        termination_obj = nb.dcim.front_ports.get(device=dev_name,name=termination_name)
    elif (termination_type == "dcim.rearport"):
        termination_obj = nb.dcim.rear_ports.get(device=dev_name,name=termination_name)

    return termination_obj

def create_nb_log(title, headerValues, nb_objs_data,headerWidthPadding=5,titleSeparaterLength=12,titleSeparaterSymbol="*"):
    """Creates a log of NetBox objects involved in a script

      Args:
        title: A string describing what the log contains
        headerValues: A list of strings indicating the columns for the log
        nb_objs_data: A list of lists of NetBox objects being outputed in log
        headerWidthPadding: A integer indicating padding around column
        titleSeparaterSymbol: A string that separates log from rest of output
        titleSeparaterLength: A integer indicating length of separator
    """
    titleSeparator=titleSeparaterLength*titleSeparaterSymbol
    numOfHeaders = len(headerValues)
    header_fmt = ""

    print()
    print(f"{titleSeparator} {title} {titleSeparator}")
    print()

    for header in headerValues:
        headerWidth = len(header) + headerWidthPadding
        header_fmt += "{:<"+str(headerWidth)+"}"

    print(header_fmt.format(*headerValues))

    for nb_obj_data in nb_objs_data:
        print(
            header_fmt.format(
                *nb_obj_data
            )
        )

    print()
