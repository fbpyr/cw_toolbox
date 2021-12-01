import sys
from pathlib import Path
from pprint import pprint, pp
from collections import namedtuple, defaultdict

import cadwork                  as cw
import attribute_controller     as ac
import element_controller       as ec
import geometry_controller      as gc
import utility_controller       as uc
import bim_controller           as bc
import material_controller      as mc
import visualization_controller as vc
import scene_controller         as sc
import file_controller          as fc
import list_controller          as lc
import shop_drawing_controller  as sdc
import menu_controller          as mec


print("\nwelcome to cw_toolbox!!\n")
print(f"running on Python {sys.version.split()[0]}")
print("\ncurrent paths available to interpreter:")
for path in sys.path:
    print(f"INFO: {path =}")

cwps = [
    r"C:\Program Files\cadwork.dir\EXE_28\Pclib.x64\python38\site-packages",
    str(Path().home() / ".virtualenvs" / "cadwork" / "Lib" / "site-packages"),
    str(Path().home() / "AppData" / "Roaming" / "Python" /
        f"Python{sys.version_info.major}{sys.version_info.minor}" / "site-packages"),
]

for cwp in cwps:
    if cwp not in sys.path:
        print(f"INFO: appending to path: {cwp}")
        sys.path.append(cwp)

import cw_toolbox
from cw_toolbox.helpers.bbox import *
from cw_toolbox.helpers.collections import *
from cw_toolbox.helpers.material import *
from cw_toolbox.helpers.param import *
from cw_toolbox.helpers.repl import *
from cw_toolbox.helpers.stubs import *
from cw_toolbox.helpers.tag import *
from cw_toolbox.helpers.visibility import *
from cw_toolbox.helpers.version import *

s0 = None
selection = ec.get_active_identifiable_element_ids()
if selection:
    s0 = selection[0]
if len(selection) > 1:
    s1 = selection[1]
selection_names = [ac.get_name(eid) for eid in selection]
print(f"\nINFO: found {len(selection) :5} selected element         - available via: selection")

all_ids = ec.get_all_identifiable_element_ids()
print(f"INFO: found {len(all_ids) :5} elements in model        - available via: all_ids")


if __name__ == "__main__":
    populate_cw_modules_catalogue(globals())

    elem_names_by_id = get_element_names_by_id(quiet=True)
    elem_ids_by_name = get_element_ids_by_name(quiet=True)
    elem_ids_by_type_name = get_element_ids_by_type_name(quiet=True)
    material_ids_by_name = get_materials_by_name()
    print(f"INFO: found {len(material_ids_by_name) :5} materials in model       - available via: material_ids_by_name")

    user_attribute_map_by_name = get_user_attribute_map_by_name()
    user_attribute_map_by_id   = get_user_attribute_map_by_id()
    print(f"INFO: found {len(user_attribute_map_by_name) :5} user attributes in model - available via: user_attribute_map_by_name\n")

    from ptpython.repl import embed

    ptp_repl = embed(globals(), locals())
    # clean up after repl session:
    del(ptp_repl)

