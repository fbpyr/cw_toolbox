# cw_toolbox
[ptpython](https://github.com/prompt-toolkit/ptpython) repl and helper modules for comfortable interactive cw python sessions


## features

* [ptpython](https://github.com/prompt-toolkit/ptpython) repl
  * paste complete scripts into the repl (if it breaks, the repl lets you inspect what went wrong <br> right at the point when 
    the error happened - similar to a break point)
  * fantastic auto-completion even into dict keys
  * repeat multi line statements in one go, not line by line
  * edit multi line statements
  * automatic doc strings (enable via `F2 - Display - Show docstring`)
  * [and more](https://github.com/prompt-toolkit/ptpython#features)
  * ...

* cw_toolbox repl
  * prepopulated variables
    * selection
      * all selected element ids: selection
      * first selected element_id: s0
      * ...
    * sorted
      * element ids per element name: elem_ids_by_name
      * ...
  * pre loaded modules
    * [cwapi3d](https://github.com/cwapi3d/cwapi3dpython) modules
    * pathlib
    * pprint, pp
    * collections.defaultdict
    * ...

* convenience [helpers](https://github.com/fbpyr/cw_toolbox/tree/main/helpers) lib (can also be use without the repl)
  * [bbox.py](https://github.com/fbpyr/cw_toolbox/blob/main/helpers/bbox.py)
    * get_bbox_from_elem_id
    * draw_line_between_bbox_centroids
    * ...
  * [collections.py](https://github.com/fbpyr/cw_toolbox/blob/main/helpers/collections.py)
    * get_element_ids_by_type_name
    * ...
  * [param.py](https://github.com/fbpyr/cw_toolbox/blob/main/helpers/param.py)
    * get_element_info
    * ...
  * [tag.py](https://github.com/fbpyr/cw_toolbox/blob/main/helpers/tag.py)
    * label_elem_with_id_text
    * ...
  * [visibility.py](https://github.com/fbpyr/cw_toolbox/blob/main/helpers/visibility.py)
    * isolate elements
    * ...


## setup / install

* Clone this repo into `..\userprofil_28\3d\API.x64` so that it becomes a native button in cw GUI.
* Symlink / clone / copy it also into a virtualenv, which is currently (will be from env vars in future) hardcoded to: <br>
  `{user_home} / .virtualenvs / cadwork / Lib / site-packages`
* Expects the dependencies listed in `requirements.txt` to be present in the above-mentioned virtualenv.

## known issues and limitations

* Only works within a cw session with the console enabled
* The console has a strange behaviour around pasting:
  * make sure the paste mode ( toggle with: `F6` ) is enabled
  * mouse right-click works for pasting
  * `Ctrl - v` or `Ctrl - Shift - v` as hotkeys for pasting do not seem to work, even with paste mode (`F6`) enabled
* The repl in its current version is modal / blocking, meaning you cannot interact with cadwork meaningfully while the 
  repl is active - quit the repl via `sys.exit()` or `rq()`
* Sometimes (~1%) it crashes cadwork - reason currently unknown

## roadmap

* show interactive model element stats from stats.py helper via altair in browser
* remove the need of a cw session with console / opening a new console on demand (help wanted)
* non-modal shell (help wanted)

## PRs and discussion in issues

* welcome!
