"""The Fusion emitter: an interpreter for the layout file (`lang.core.layout_types`).

Two halves:

- `plan` turns a layout into the geometry the emitter draws, in world
  millimetres: outlines as 3D rings, operations batched per face and depth,
  chamfers as contours to find edges along. Plain Python, unit tested.
- `fusion` draws a plan into a Fusion document with Fusion's own features.
  The only module in the language that imports `adsk`.

Fusion's Python has no shapely, so `lang` itself cannot be imported there.
Load this sub-package without its parent, from an MCP script or an add-in::

    import importlib, importlib.util, sys
    repo = '/path/to/fusion-addins'
    for name in [n for n in sys.modules if n.startswith('lang.emit')]:
        del sys.modules[name]                      # pick up edits on re-run
    spec = importlib.util.spec_from_file_location(
        'lang.emit', repo + '/lang/emit/__init__.py',
        submodule_search_locations=[repo + '/lang/emit'])
    pkg = importlib.util.module_from_spec(spec)
    sys.modules['lang.emit'] = pkg
    spec.loader.exec_module(pkg)
    emit = importlib.import_module('lang.emit.fusion')
    report = emit.emit_file(repo + '/out/layout.json')

(`from lang.emit import fusion` would try to import the parent `lang`;
`import_module` only needs `lang.emit` in `sys.modules`.)
"""
