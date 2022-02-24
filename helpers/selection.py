import element_controller    as ec
import visibility_controller as vc


def deactivate_all():
    """
    Convenience function deactivate/deselect all.
    :return:
    """
    vc.set_inactive(ec.get_all_identifiable_element_ids())


def activate(elem_id: int):
    """
    Convenience function to active/select element by id.
    :return:
    """
    vc.set_active(elem_id)

