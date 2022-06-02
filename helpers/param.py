import json
from pathlib import Path
from functools import lru_cache
import attribute_controller     as ac
import bim_controller           as bc
import geometry_controller      as gc
import utility_controller       as uc
import visualization_controller as vc


def get_element_info(elem_id: int) -> dict:
    """
    Get a base set of element information
    :param elem_id:
    :return:
    """
    element_info = {
        "id"           : elem_id,
        "name"         : ac.get_name(elem_id),
        "comment"      : ac.get_comment(elem_id),
        "group"        : ac.get_group(elem_id),
        "subgroup"     : ac.get_subgroup(elem_id),
        "material_name": ac.get_element_material_name(elem_id),
        "color_index"  : vc.get_color(elem_id),
        "building_name": bc.get_building(elem_id),
        "storey_name"  : bc.get_storey(elem_id),
        "length"       : gc.get_length(elem_id),
        "width"        : gc.get_width(elem_id),
        "height"       : gc.get_height(elem_id),
        "volume"       : gc.get_volume(elem_id),
    }
    if get_element_type_info(elem_id):
        element_info["type_info"] = get_element_type_info(elem_id)[0]
    else:
        element_info["type_info"] = ""
    if get_element_ifc_type_info(elem_id):
        element_info["ifc_type_info"] = get_element_ifc_type_info(elem_id)[0]
    else:
        element_info["ifc_type_info"] = ""
    return element_info


def get_element_type_info(elem_id: int) -> list:
    """
    Iterates over element type attributes to retrieve information
    :param elem_id:
    :return:
    """
    type_info = []
    element_type = ac.get_element_type(elem_id)
    for attr in dir(element_type):
        if attr.startswith("is_"):
            attr_value = getattr(element_type, attr)()
            #print(attr, attr_value)
            if attr_value:
                type_info.append(attr[3:])
    return type_info


def get_element_ifc_type_info(elem_id: int) -> list:
    """
    Iterates over element ifc type attributes to retrieve information
    :param elem_id:
    :return:
    """
    type_info = []
    element_type = bc.get_ifc2x3_element_type(elem_id)
    for attr in dir(element_type):
        if attr == "is_none":
            continue
        if attr.startswith("is_"):
            attr_value = getattr(element_type, attr)()
            #print(attr, attr_value)
            if attr_value:
                type_info.append(attr[3:])
    return type_info


def get_element_user_attributes(elem_id: int) -> dict:
    """
    Returns a mapping of parameter name - value
    for user attributes of specified element.
    :param elem_id:
    :return:
    """
    user_param_map = {}
    user_attribute_map_by_name = get_user_attribute_map_by_name()
    for name, i in user_attribute_map_by_name.items():
        attr_value = ac.get_user_attribute(elem_id, i)
        user_param_map[i] = {
            "name" : name,
            "value": attr_value,
        }
    return user_param_map


def ensure_user_parameters(path_override=None, quiet=None) -> dict:
    """
    Ensures that the canonical mapping of user parameters
    according to a single source are set.
    :return:
    """
    if path_override:
        user_profile_path = Path(path_override)
    else:
        user_profile_path = Path(uc.get_3d_userprofil_path())
    company_user_profile_path = user_profile_path / "company_user_attributes.json"
    if not company_user_profile_path.exists():
        print(f"ERROR: Sorry {company_user_profile_path} seems to be missing")
        return {}
    with open(company_user_profile_path) as attr_json:
        cw_attributes = json.load(attr_json)["cw_user_attributes"]

    for attr_name, cw_user_attr_nr in cw_attributes.items():
        if ac.get_user_attribute_name(cw_user_attr_nr) == f"User{cw_user_attr_nr}":
            ac.set_user_attribute_name(cw_user_attr_nr, attr_name)
            if not quiet:
                print(f"INFO: ensure_user_parameters: successfully set user attribute: {attr_name}")
        elif ac.get_user_attribute_name(cw_user_attr_nr) == attr_name:
            if not quiet:
                print(f"INFO: ensure_user_parameters: user attribute already set: {attr_name}")
            continue
        else:
            if not quiet:
                print(f"INFO: ensure_user_parameters: user attribute {cw_user_attr_nr} named {attr_name} already in use!")
    return cw_attributes


@lru_cache(maxsize=128)
def get_user_attribute_map_by_name() -> dict:
    """
    Get user attribute mapping by attribute names
    :return:
    """
    user_attribute_name_map = {}
    for i in range(USER_ATTRIBUTE_SEARCH_COUNT):
        attr_name = ac.get_user_attribute_name(i)
        if attr_name.startswith("User"):
            continue
        user_attribute_name_map[attr_name] = i
    return user_attribute_name_map


@lru_cache(maxsize=128)
def get_user_attribute_map_by_id() -> dict:
    """
    Get user attribute mapping by attribute id
    :return:
    """
    user_attribute_id_map = {}
    for i in range(USER_ATTRIBUTE_SEARCH_COUNT):
        attr_name = ac.get_user_attribute_name(i)
        if attr_name.startswith("User"):
            continue
        user_attribute_id_map[i] = attr_name
    return user_attribute_id_map


def get_element_attribute_value(elem_id: int, attr_name: str):
    """
    Retrieves Attribute value for element attribute or user_attribute
    :param elem_id:
    :param attr_name:
    :return:
    """
    if   attr_name == "cadwork_Id"          : return elem_id
    elif attr_name == "Name"                : return ac.get_name(elem_id)
    elif attr_name == "Farbe"               : return vc.get_color(elem_id)
    elif attr_name == "Länge"               : return gc.get_length(elem_id)
    elif attr_name == "Breite"              : return gc.get_width(elem_id)
    elif attr_name == "Höhe"                : return gc.get_height(elem_id)
    elif attr_name == "Gruppe"              : return ac.get_group(elem_id)
    elif attr_name == "Bauuntergruppe"      : return ac.get_subgroup(elem_id)
    elif attr_name == "Bemerkung"           : return ac.get_comment(elem_id)
    elif attr_name == "Nr.Produktionsliste" : return ac.get_production_number(elem_id)
    elif attr_name == "Nr.Stückliste"       : return ac.get_part_number(elem_id)

    elif USER_ATTRIBUTE_MAP_BY_NAME.get(attr_name):
        # print(f"found in user_attribute_map: {attr_name =}")
        user_attr_id = USER_ATTRIBUTE_MAP_BY_NAME[attr_name]
        return ac.get_user_attribute(elem_id, user_attr_id)

    else:
        print(f"could not find attribute: {attr_name =}")


def set_element_attribute_value(elem_id: int, attr_name: str, attr_value: str):
    """
    Sets Attribute value for element attribute or user_attribute, where it makes sense.
    Value type conversions - which have the potential to fail - are attempted where necessary.
    :param elem_id: int
    :param attr_name: str
    :return:
    """
    if   attr_name == "Name"                : return ac.set_name(elem_id, attr_value)
    elif attr_name == "Farbe"               : return vc.set_color(elem_id, int(attr_value))
    elif attr_name == "Gruppe"              : return ac.set_group(elem_id, attr_value)
    elif attr_name == "Bauuntergruppe"      : return ac.set_subgroup(elem_id, attr_value)
    elif attr_name == "Bemerkung"           : return ac.set_comment(elem_id, attr_value)
    #elif attr_name == "Nr.Produktionsliste" : return ac.get_production_number(elem_id)
    #elif attr_name == "Nr.Stückliste"       : return ac.get_part_number(elem_id)

    elif USER_ATTRIBUTE_MAP_BY_NAME.get(attr_name):
        # print(f"found in user_attribute_map: {attr_name =}")
        user_attr_id = USER_ATTRIBUTE_MAP_BY_NAME[attr_name]
        return ac.set_user_attribute(elem_id, user_attr_id, attr_value)

    else:
        print(f"could not find attribute: {attr_name =}")


USER_ATTRIBUTE_SEARCH_COUNT = 399

USER_ATTRIBUTE_MAP_BY_NAME = get_user_attribute_map_by_name()
USER_ATTRIBUTE_MAP_BY_ID   = get_user_attribute_map_by_id()

UNIVERSAL_ATTR_SETTER_IMPLEMENTED = [
    "Name",
    "Farbe",
    "Gruppe",
    "Bauuntergruppe",
    "Bemerkung",
]

