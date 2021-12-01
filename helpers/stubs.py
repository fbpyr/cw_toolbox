import datetime
from .version import get_cw_version_info


def populate_cw_modules_catalogue(repl_globals: dict):
    """
    Inspects the available cwapi modules and registers them into cw_modules dictionary.
    :return:
    """
    for module_name, methods_by_name in cw_modules.items():
        cw_module = repl_globals[module_name]
        cw_modules_by_name[module_name] = cw_module
        for item_name in dir(cw_module):
            method = getattr(cw_module, item_name)
            if not str(method).startswith(PY_CAPSULE_METHOD_TYPE_STR):
                continue
            methods_by_name[f"{module_name}.{method.__name__}"] = method.__doc__


def find_cw_methods(search_name:str):
    """
    Searches for cwapi methods, results are shown in console.
    :param search_name:
    :return:
    """
    for module_name, methods_by_name in cw_modules.items():
        for method_name in methods_by_name:
            if search_name in method_name:
                print(f"\n{module_name}:")
                print(f"  {module_name}.{methods_by_name[method_name].strip()}")


def show_methods_in_module(module_name):
    """
    Lists all methods and their doc strings in cwapi module.
    :param module_name:
    :return:
    """
    if not cw_modules.get(module_name):
        print(f"sorry, could not find module: {module_name}")
        return
    print(f"\n==== {module_name}:\n")
    for name, doc_string in cw_modules[module_name].items():
        print(f"  {name}\n    {doc_string}")


def list_searched_modules():
    """
    Lists all searced cwapi modules by helpers.stubs
    :return:
    """
    print("\nsearched modules:")
    for module_name, mod in cw_modules_by_name.items():
        print(f"  {mod.__name__ :25} as {module_name}")


def generate_markdown(repl_globals: dict, markdown_path=None):
    """
    Generates stubs markdown od available cwapi functionality
    :param repl_globals:
    :param markdown_path:
    :return:
    """
    cw_version_info = get_cw_version_info()
    if not markdown_path:
        markdown_path = "cw_module_stubs.md"
    md_str = "# cwapi method stubs\n"
    md_str += f"generated from version: {cw_version_info['version']} build: {cw_version_info['build']}\n<br>"
    md_str += f"generated at {datetime.datetime.now()}\n<br>"
    md_str += f"{len(cw_modules)} modules found for cwapi\n"
    for module_name, _ in cw_modules.items():
        mod = repl_globals[module_name]
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
cw_modules_by_name = {}
