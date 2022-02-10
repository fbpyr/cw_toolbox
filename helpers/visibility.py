import element_controller       as ec
import visualization_controller as vc


def isolate_elements(elem_ids):
    """
    Isolates specified elements in view.
    All other elements are set to invisible.
    :param elem_ids: element ids to isolate.
    :return:
    """
    vc.set_invisible(ec.get_all_identifiable_element_ids())
    vc.set_visible(elem_ids)


def refresh():
    """
    Convenience function to refresh active view.
    :return:
    """
    vc.refresh()

