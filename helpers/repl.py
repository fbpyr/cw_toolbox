import sys
from tkinter import Tk, Label
import element_controller       as ec
import visualization_controller as vc


def reset():
    """
    shortcut to delete all elements in model - DANGER!!
    :return:
    """
    ec.delete_elements(ec.get_all_identifiable_element_ids())
    vc.refresh()


def interrupt_repl():
    """
    Blocks repl session with tkinter helper to access cadwork application.
    Resumes the repl session on closing the tkinter helper.
    :return:
    """
    window = Tk()
    window.geometry("400x100")
    window.title("Close this window resume repl session")
    window.config(background="#666666")
    cw_style = {
        "font": ("Arial", 10),
        "bg": "#666666",
        "fg": "#ffffff",
    }
    text = "This blocks the current repl session.\n"\
           "Close this window resume repl session."
    label = Label(
        master=window,
        text=text,
        **cw_style
    )
    label.pack(padx=5, pady=5, anchor="w")
    window.mainloop()


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

