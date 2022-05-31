from tkinter import Tk, Label, BooleanVar, Checkbutton


def tk_checkbox_list_gui(element_names, title="tk_window_title", header="list_header:"):
    """
    Displays a tkinter list with two columns for element and checkbox.
    User selection is returned as dict.
    :param element_names:
    :param title:
    :param header:
    :return:
    """
    window = Tk()
    element_count = len(element_names)
    window.geometry(f"320x{30 + 38 * element_count}")
    window.title(title)
    window.config(background=BACKGROUND_COLOR)
    widget_options = WIDGET_OPTIONS.update({"master": window})
    Label(
        text=header,
        **widget_options,
        anchor="w",
    ).grid(row=0, column=0, **WIDGET_PLACEMENT_OPTIONS)

    element_chosen_map = {}
    for i, name in enumerate(element_names):
        Label(
            text=name,
            **widget_options,
            anchor="w",
        ).grid(row=i+1, column=0, **WIDGET_PLACEMENT_OPTIONS)
        element_chosen_map[name] = BooleanVar()
        Checkbutton(
            variable=element_chosen_map[name],
            onvalue=1,
            offvalue=0,
            activebackground=BACKGROUND_COLOR,
            selectcolor=BACKGROUND_COLOR,
            **widget_options,
        ).grid(row=i+1, column=1, **WIDGET_PLACEMENT_OPTIONS)

    window.mainloop()
    return {k:None for k,v in element_chosen_map.items()}


BACKGROUND_COLOR = "#666666"
WIDGET_OPTIONS = {
    "bg": BACKGROUND_COLOR,
    "fg": "#ffffff",
    "font": ("Arial", 10),
}
WIDGET_PLACEMENT_OPTIONS = {
    "padx": 11,
    "pady": 5,
    "sticky": 'nsew',
}
