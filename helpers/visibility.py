import element_controller       as ec
import visualization_controller as vc


def isolate_elements(elem_ids):
    """
    Isolates specified elements in view.
    All other elements are set to invisible.
    :param elem_ids: element ids to isolate.
    :return:
    """
    all_ids = ec.get_all_identifiable_element_ids()
    hide_ids = []
    for elem_id in all_ids:
        if elem_id not in elem_ids:
            hide_ids.append(elem_id)
    vc.set_invisible(hide_ids)
    vc.set_visible(elem_ids)
