from tkinter import Tk, Label, BooleanVar, Checkbutton, StringVar, OptionMenu, Button, Event, INSERT, Text


def _tk_window_exit(window: Tk):
    """
    Internal: Convenience callback function to close a tk window.
    :param window:
    :return:
    """
    window.quit()
    window.destroy()


def _tk_apply_or_abort(window: Tk, choice: dict, action: str):
    """
    Internal: Convenience callback function for 'Cancel' or 'Ok' and exit.
    :param window:
    :param choice:
    :param action:
    :return:
    """
    # print(f"{selection['selected_attr'] =}")
    if action == "apply":
        choice["selected"] = choice["selected_attr"].get()
        # print(f"{action =} {choice['selected'] =}")
    elif action == "abort":
        choice["selected"] = ""
    _tk_window_exit(window)


def _tk_selector_key_binds(event: Event, choice: dict, all_choices: list):
    """
    Internal: Adds hotkey 1-9 to select dropdown value.
    :param event:
    :param choice:
    :param all_choices:
    :return:
    """
    # print(event, event.char, event.keycode, 'is pressed')
    if event.keycode in KEY_CODES_1_to_9:
        key_number = event.keycode-48
        # print(f"keycode: {key_number} was pressed: {event.keysym}")
        if key_number < len(all_choices):
            choice["selected_attr"].set(all_choices[event.keycode-48])


def _tk_toggle_list_item(event: Event, element_tk_var_by_id: dict):
    """
    Internal: Adds hotkey 1-9 to toggle checkbox list items.
    :param event:
    :param element_tk_var_by_id:
    :return:
    """
    # print(event, event.char, event.keycode, 'is pressed')
    if event.keycode in KEY_CODES_1_to_9:
        key_number = event.keycode - 48
        elem_index = key_number - 1
        # print(f"keycode: {key_number} was pressed: {event.keysym}")
        if key_number < len(element_tk_var_by_id):
            current_value = element_tk_var_by_id[elem_index].get()
            # print(f"{current_value =}")
            element_tk_var_by_id[elem_index].set(not current_value)


def tk_checkbox_list_gui(element_names, title="tk_window_title", header="list_header:") -> dict:
    """
    Displays a list of selectable elements with two columns for element name and checkbox.
    User selection is returned as dict.
    :param element_names: List[str]
    :param title: str
    :param header: str
    :return: dict
    """
    window = Tk()
    element_count = len(element_names)
    window.geometry(f"320x{30 + 38 * element_count}")
    window.title(title)
    window.config(background=BACKGROUND_COLOR)
    widget_options = {"master": window}
    widget_options.update(WIDGET_OPTIONS)

    Label(
        text=header,
        **widget_options,
        anchor="w",
    ).grid(row=0, column=0, **WIDGET_PLACEMENT_OPTIONS)

    element_chosen_map = {}
    element_tk_var_by_id = {}
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
        element_tk_var_by_id[i] = element_chosen_map[name]

    window.bind(sequence='<Return>', func=lambda ev: _tk_window_exit(window))
    window.bind(sequence='<Escape>', func=lambda ev: _tk_window_exit(window))
    window.bind(sequence='<Key>'   , func=lambda ev: _tk_toggle_list_item(ev, element_tk_var_by_id))

    window.focus_force()
    window.mainloop()
    return {k:v.get() for k,v in element_chosen_map.items()}


def tk_dropdown(choices, title="tk_window_title", header="list_header:") -> str:
    """
    Displays a tkinter dropdown with the supplied choices.
    User selection is returned as string.
    :param choices:
    :param title:
    :param header:
    :return:
    """
    window = Tk()
    window.geometry("390x140")
    window.title(title)
    window.config(background=BACKGROUND_COLOR)
    widget_options = {"master": window}
    widget_options.update(WIDGET_OPTIONS)

    Label(
        text=header,
        **widget_options,
        anchor="w",
    ).grid(row=0, column=0, **WIDGET_PLACEMENT_OPTIONS)

    choice = {
        "default"      : "Bitte w??hlen",
        "selected"     : "",
        "selected_attr": StringVar(),
    }

    all_choices = [choice["default"]]
    all_choices.extend(choices)
    choice["selected_attr"].set("Bitte w??hlen")

    attr_selector = OptionMenu(
        window,
        choice["selected_attr"],
        *all_choices,
    )
    attr_selector.config(ATTR_SELECTOR_CONFIG)
    attr_selector["menu"].config(ATTR_SELECTOR_MENU_CONFIG)
    attr_selector.grid(row=0, column=1, **WIDGET_PLACEMENT_OPTIONS)

    apply_choice = Button(
        text="Anwenden",
        command=lambda: _tk_apply_or_abort(window, choice, "apply"),
        **widget_options,
    )
    apply_choice.grid(row=2, column=1, **WIDGET_PLACEMENT_OPTIONS)

    abort = Button(
        text="Abbrechen",
        command=lambda: _tk_apply_or_abort(window, choice, "abort"),
        **widget_options,
    )
    abort.grid(row=1, column=1, **WIDGET_PLACEMENT_OPTIONS)

    window.bind(sequence='<Key>'   , func=lambda ev: _tk_selector_key_binds(ev, choice, all_choices))
    window.bind(sequence='<Return>', func=lambda ev: _tk_apply_or_abort(window, choice, "apply"))
    window.bind(sequence='<Escape>', func=lambda ev: _tk_apply_or_abort(window, choice, "abort"))

    window.focus_force()
    window.mainloop()

    if choice["selected"] == choice["default"]:
        choice["selected"] = ""
    return choice["selected"]


def tk_show_list_gui(text, title="tk_window_title", header="list_header:"):
    """
    Displays a tkinter gui with the supplied text.
    :param text:
    :return:
    """
    window = Tk()
    window.geometry("300x230")
    window.title(title)
    window.config(background="#666666")
    widget_template = {
        "master": window,
        "font": ("Arial", 10),
        "bg": "#666666",
        "fg": "#ffffff",
    }
    label = Label(
        text=header,
        **widget_template,
    )
    label.grid(row=1, column=1, sticky='nsew')

    text_field = Text(
        width=39,
        height=11,
        **widget_template,
    )
    text_field.grid(row=3, column=1, sticky='nsew', padx=11, pady=5)
    text_field.insert(INSERT, text)

    window.mainloop()



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
ATTR_SELECTOR_CONFIG = {
    "activebackground": "#666666",
    "bg": BACKGROUND_COLOR,
    "fg": "#ffffff",
    "font": ("Arial", 10),
    "highlightthickness": 0,
    "width": 14,
}
ATTR_SELECTOR_MENU_CONFIG = {
    "bg": BACKGROUND_COLOR,
    "fg": "#ffffff",
    "font": ("Arial", 10),
    "activeborderwidth": 0,
    "borderwidth": 0,
}
#                  ( 1,  2,  3,  4,  5,  6,  7,  8,  9)
KEY_CODES_1_to_9 = (49, 50, 51, 52, 53, 54, 55, 56, 57)

