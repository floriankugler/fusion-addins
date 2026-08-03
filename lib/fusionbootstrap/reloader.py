"""Self-reload support for add-ins during development.

Event handlers registered from an externally executed script (e.g. via the
Fusion MCP server) are torn down when that script execution ends - an add-in
restarted that way has dead UI buttons. This module registers a custom event
when Fusion itself starts the add-in (a persistent context). External tooling
fires the event to restart the add-in; the reload then runs inside the
add-in's own handler, so the re-registered UI handlers survive.

This module lives in fusionbootstrap on purpose: it is excluded from the
dev-mode module reload, so the registrations and results survive reloads.
"""

import adsk.core
import traceback

_registrations: dict[str, tuple] = {}
_results: dict[str, str] = {}
_counters: dict[str, int] = {}


def ensure(event_id: str, addin_entry: str):
    """Register the reload custom event for an add-in.

    Always re-registers: stopping an add-in via the Scripts and Add-Ins dialog
    makes Fusion unregister its custom events, so a surviving _registrations
    entry does not mean the event is still alive. Skipping re-registration here
    left dead events behind after a manual stop/start cycle.
    """
    _registrations.pop(event_id, None)
    app = adsk.core.Application.get()
    try:
        app.unregisterCustomEvent(event_id)
    except Exception:
        pass
    event = app.registerCustomEvent(event_id)

    class ReloadHandler(adsk.core.CustomEventHandler):
        def notify(self, args):
            from . import bootstrap
            count = _counters.get(event_id, 0) + 1
            _counters[event_id] = count
            try:
                bootstrap.stop(None, addin_entry)
                bootstrap.run(None, addin_entry)
                _results[event_id] = f'ok #{count}'
            except Exception:
                _results[event_id] = f'error #{count}: {traceback.format_exc()}'

    handler = ReloadHandler()
    event.add(handler)
    _registrations[event_id] = (event, handler)


def last_result(event_id: str) -> str | None:
    """Result marker of the most recent reload ('ok #n' or 'error #n: ...')."""
    return _results.get(event_id)
