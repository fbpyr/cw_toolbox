def populate_cw_modules_catalogue():
    """
    Inspects the available cwapi modules and registers them into cw_modules dictionary.
    :return:
    """
    cw_modules = {
        "ac": {},
        "bc": {},
        "cw": {},
        "ec": {},
        "fc": {},
        "gc": {},
        "lc": {},
        "mc": {},
        "mec": {},
        "sc": {},
        "sdc": {},
        "uc": {},
        "vc": {},
    }
    for module_name, methods_by_name in cw_modules.items():
        cw_module = globals()[module_name]
        for item_name in dir(cw_module):
            method = getattr(cw_module, item_name)
            if not str(method).startswith(PY_CAPSULE_METHOD_TYPE_STR):
                continue
            methods_by_name[f"{module_name}.{method.__name__}"] = method.__doc__


def find_cw_methods(search_name):
    """
    Searches for cwapi methods, results are shown in console.
    :param search_name:
    :return:
    """
    for module_name, methods_by_name in cw_modules.items():
        cw_module = globals()[module_name]
        for method_name in methods_by_name:
            if search_name in method_name:
                print(f"\n{cw_module.__name__}:")
                print(f"  {module_name}.{methods_by_name[method_name].strip()}")


def generate_markdown(markdown_path=None):
    """
    Generates stubs markdown od available cwapi functionality
    :param markdown_path:
    :return:
    """
    if not markdown_path:
        markdown_path = "cw_module_stubs.md"
    md_str = "# cwapi method stubs\n"
    md_str += f"{len(cw_modules)} modules found for cwapi\n"
    for module_name, _ in cw_modules.items():
        mod = globals()[module_name]
        md_str += f"\n## {mod.__name__} as {module_name}\n"
        for e in dir(mod):
            func = getattr(mod, e)
            if not str(func).startswith(PY_CAPSULE_METHOD_TYPE_STR):
                continue
            method_doc_str = func.__doc__.strip().replace("(", "(\n      ").replace(")", "\n  )").replace(", ", ",\n      ")
            md_str += f"\n* {mod.__name__}.{func.__name__}\n  ```\n  {module_name}.{method_doc_str}\n  ```\n"
    with open(markdown_path, "w") as md:
        md.write(md_str)


PY_CAPSULE_METHOD_TYPE_STR = "<built-in method"
cw_modules = populate_cw_modules_catalogue(cw_modules)
