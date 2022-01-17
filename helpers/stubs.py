import types
import datetime
from .version import get_cw_version_info


def populate_cw_modules_catalogue(repl_globals: dict):
    """
    Inspects the available cwapi modules and registers them into cw_modules dictionary.
    :return:
    """
    for module_alias, methods_by_name in cw_modules.items():
        cw_module = repl_globals[module_alias]
        cw_module_name = cw_module.__name__
        cw_modules_by_name[cw_module_name] = cw_module
        cw_modules_by_module_aliases[module_alias] = cw_module
        cw_module_alias_by_name[cw_module_name] = module_alias
        for item_name in dir(cw_module):
            method = getattr(cw_module, item_name)
            if not str(method).startswith(PY_CAPSULE_METHOD_TYPE_STR):
                continue
            methods_by_name[f"{module_alias}.{method.__name__}"] = method.__doc__


def find_cwapi_modules():
    """
    Lists all searced cwapi modules by helpers.stubs
    :return:
    """
    print(f"\n{len(cw_modules)} modules found in cwapi\n")
    for module_alias, method_infos in cw_modules.items():
        module_name = cw_modules_by_module_aliases[module_alias].__name__
        print(f"  {len(method_infos.values()) :3} methods in:  {module_name :25} as {module_alias}")


def find_methods_in_module(module_or_module_alias):
    """
    Lists all methods and their doc strings in cwapi module.
    :param module_or_module_alias:
    :return:
    """
    if isinstance(module_or_module_alias, types.ModuleType):
        module = module_or_module_alias
        module_alias = cw_module_alias_by_name[cw_modules_by_name[module.__name__].__name__]
    elif isinstance(module_or_module_alias, str):
        if cw_module_alias_by_name.get(module_or_module_alias):
            module_alias = cw_module_alias_by_name[module_or_module_alias]
        else:
            module_alias = module_or_module_alias
    if not cw_modules.get(module_alias):
        print(f"sorry, could not find module: {module_alias}")
        return
    module_name = cw_modules_by_module_aliases[module_alias].__name__
    print(f"\n==== {len(cw_modules[module_alias].values())} methods in {module_name} as {module_alias}:\n")
    for name, doc_string in cw_modules[module_alias].items():
        print(f"  {name}\n    {doc_string}")


def find_text_in_cwapi_methods(search_text:str):
    """
    Searches for methods in cwapi modules by search, results are shown in console.
    :param search_text:
    :return:
    """
    for module_name, methods_by_name in cw_modules.items():
        for method_name in methods_by_name:
            if search_text in method_name:
                print(f"\n{module_name}:")
                print(f"  {module_name}.{methods_by_name[method_name].strip()}")


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
    md_str += f"{len(cw_modules)} modules found in cwapi\n"
    for module_alias, method_infos in cw_modules.items():
        module_name = cw_modules_by_module_aliases[module_alias].__name__
        md_str += f"\n## ({len(method_infos)}) {module_name} as {module_alias}\n"
        for method_name, method_doc_str in method_infos.items():
            method_doc_str = method_doc_str.strip(
                ).replace("(", "(\n      "
                ).replace(")", "\n  )"
                ).replace(", ", ",\n      ")
            md_str += f"\n* {module_name}.{method_name}\n  ```\n  {module_alias}.{method_doc_str}\n  ```\n"
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
cw_modules_by_module_aliases = {}
cw_modules_by_name = {}
cw_module_alias_by_name = {}
