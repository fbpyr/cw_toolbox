from dataclasses import dataclass

import cadwork             as cw
import element_controller  as ec
import geometry_controller as gc


@dataclass
class Bbox:
    points:   list
    min_pt:   cw.point_3d
    max_pt:   cw.point_3d
    centroid: cw.point_3d


def get_bbox_from_elem_id(elem_id: int) -> Bbox:
    """
    Returns orthogonal bounding box for element of specified id.
    :param elem_id:
    :return:
    """
    pts = gc.get_element_vertices(elem_id)
    x_min = min([pt.x for pt in pts])
    y_min = min([pt.y for pt in pts])
    z_min = min([pt.z for pt in pts])
    min_pt = cw.point_3d(x_min, y_min, z_min)
    x_max = max([pt.x for pt in pts])
    y_max = max([pt.y for pt in pts])
    z_max = max([pt.z for pt in pts])
    max_pt = cw.point_3d(x_max, y_max, z_max)
    centroid = (max_pt - min_pt) / 2 + min_pt
    return Bbox(pts, min_pt, max_pt, centroid)


def get_bbox_from_points(points: list) -> Bbox:
    """
    Returns orthogonal bounding box for collection of points.
    :param points:
    :return:
    """
    x_min = min([pt.x for pt in points])
    y_min = min([pt.y for pt in points])
    z_min = min([pt.z for pt in points])
    min_pt = cw.point_3d(x_min, y_min, z_min)
    x_max = max([pt.x for pt in points])
    y_max = max([pt.y for pt in points])
    z_max = max([pt.z for pt in points])
    max_pt = cw.point_3d(x_max, y_max, z_max)
    points = (
        cw.point_3d(x_min, y_min, z_min),
        cw.point_3d(x_max, y_min, z_min),
        cw.point_3d(x_max, y_max, z_min),
        cw.point_3d(x_min, y_max, z_min),
        cw.point_3d(x_min, y_min, z_max),
        cw.point_3d(x_max, y_min, z_max),
        cw.point_3d(x_max, y_max, z_max),
        cw.point_3d(x_min, y_max, z_max),
    )
    centroid = (max_pt - min_pt) / 2 + min_pt
    return Bbox(points, min_pt, max_pt, centroid)


def is_point_in_bbox(point: cw.point_3d, bbox: Bbox) -> bool:
    """
    Checks whether a given point is within a given bounding box
    :param point:
    :param bbox:
    :return:
    """
    x, y, z = (point.x, point.y, point.z)
    bbx_max_x, bbx_max_y, bbx_max_z = (bbox.max.x, bbox.max.y, bbox.max.z)
    bbx_min_x, bbx_min_y, bbx_min_z = (bbox.min.x, bbox.min.y, bbox.min.z)
    if bbx_max_x > x > bbx_min_x and \
       bbx_max_y > y > bbx_min_y and \
       bbx_max_z > z > bbx_min_z:
        return True
    return False


def bbox_longest_ortho_edge_vector(bbox: Bbox):
    """
    Checks for axis of the longest orthogonal edge of bbox
    :param bbox:
    :return: str
    """
    axes_lengths = {
        "x" : abs(bbox.max.x - bbox.min.x),
        "y" : abs(bbox.max.y - bbox.min.y),
        "z" : abs(bbox.max.z - bbox.min.z),
    }
    return max(axes_lengths, key=axes_lengths.get)


def draw_line_between_bbox_centroids(elem_id_one: int, elem_id_two: int):
    """
    Draws a line between the bounding box centroids of two elements
    :param elem_id_one:
    :param elem_id_two:
    :return:
    """
    elem_one_centroid = get_bbox_from_elem_id(elem_id_one).centroid
    elem_two_centroid = get_bbox_from_elem_id(elem_id_two).centroid
    line = ec.create_line_points(elem_one_centroid, elem_two_centroid)
    return line


def draw_bbox_surfaces(bbox: Bbox) -> list:
    """
    Draws surfaces on the bounding box faces
    :param bbox:
    :return:
    """
    points = bbox.points
    surfaces = []
    surface_point_indices = (
        (0,1,2,3),
        (4,5,6,7),
        (0,1,5,4),
        (2,3,7,6),
        (1,2,6,5),
        (0,3,7,4),
    )
    for indices in surface_point_indices:
        surface_points = [points[idx] for idx in indices]
        surface_id = ec.create_surface(surface_points)
        surfaces.append(surface_id)

    return surfaces

