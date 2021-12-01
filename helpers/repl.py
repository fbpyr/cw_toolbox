import sys
import element_controller       as ec
import visualization_controller as vc


def reset():
    """
    shortcut to delete all elements in model
    :return:
    """
    ec.delete_elements(ec.get_all_identifiable_element_ids())
    vc.refresh()


def rq():
    """
    shortcut to quit the repl
    :return:
    """
    quit_repl()


def qr():
    """
    shortcut to quit the repl
    :return:
    """
    quit_repl()


def qq():
    """
    shortcut to quit the repl
    :return:
    """
    quit_repl()


def quit_repl():
    """
    shortcut to quit the repl
    :return:
    """
    sys.exit()

