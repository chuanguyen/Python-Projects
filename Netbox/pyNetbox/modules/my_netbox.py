#!/usr/bin/env python

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
            nb_obj = nb.ipam.vrfs.get(name=searchTeam_modified)

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