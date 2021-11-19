import element_controller       as ec
import geometry_controller      as gc


def label_elem_with_id_text(elem_id, text_size=None):
    """
    Adds 3d id text label to centroid of given element ids.
    :param elem_id:
    :param text_size:
    :return:
    """
    return label_elem_with_text(elem_id, str(elem_id), text_size=None)


def label_elem_with_text(elem_id, text, text_size=None):
    """
    Adds 3d text label with given text to centroid of given element ids.
    :param elem_id:
    :param text:
    :param text_size:
    :return:
    """
    return ec.create_text_object(
        text,
        gc.get_center_of_gravity(elem_id),
        gc.get_local_x(),
        gc.get_local_y(),
        text_size or 250,
    )

