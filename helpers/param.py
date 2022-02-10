import json
from pathlib import Path
from functools import lru_cache
import attribute_controller     as ac
import utility_controller       as uc
import bim_controller           as bc
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


USER_ATTRIBUTE_SEARCH_COUNT = 399
