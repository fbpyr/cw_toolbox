import material_controller as mc


def get_materials_by_name() -> dict:
    """
    Retrieves materials of model by name
    :return:
    """
    material_ids_by_name = {}
    for material_id in mc.get_all_materials():
        mat_name = mc.get_name(material_id)
        material_ids_by_name[mat_name] = material_id
    return material_ids_by_name

