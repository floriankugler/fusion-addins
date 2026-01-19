# UserInterface.workspacePreDeactivate Event

Parent Object: [UserInterface](UserInterface.md)  

## Description

The workspacePreDeactivate event fires at the VERY start of a workspace being deactivated. The client can add or remove WorkspaceEventHandlers from the WorkspaceEvent.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "userInterface_var" is a variable referencing a UserInterface object.
# "MyWorkspacePreDeactivateHandler" is the name of the class that handles the event.
onWorkspacePreDeactivate = MyWorkspacePreDeactivateHandler()
userInterface_var.workspacePreDeactivate.add(onWorkspacePreDeactivate)
handlers.append(onWorkspacePreDeactivate)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the workspacePreDeactivate event.
class MyWorkspacePreDeactivateHandler(adsk.core.WorkspaceEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.WorkspaceEventArgs):
        # Code to react to the event.
        app.log('In MyWorkspacePreDeactivateHandler event handler.')
```

## Property Value

This is an event property that returns a [WorkspaceEvent](WorkspaceEvent.md).

## Version

Introduced in version March 2015  

