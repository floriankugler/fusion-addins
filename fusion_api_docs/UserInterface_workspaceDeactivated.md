# UserInterface.workspaceDeactivated Event

Parent Object: [UserInterface](UserInterface.md)  

## Description

The workspaceDeactivated event fires at the VERY end of a workspace being deactivated. The client can add or remove WorkspaceEventHandlers from the WorkspaceEvent.

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
# "MyWorkspaceDeactivatedHandler" is the name of the class that handles the event.
onWorkspaceDeactivated = MyWorkspaceDeactivatedHandler()
userInterface_var.workspaceDeactivated.add(onWorkspaceDeactivated)
handlers.append(onWorkspaceDeactivated)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the workspaceDeactivated event.
class MyWorkspaceDeactivatedHandler(adsk.core.WorkspaceEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.WorkspaceEventArgs):
        # Code to react to the event.
        app.log('In MyWorkspaceDeactivatedHandler event handler.')
```

## Property Value

This is an event property that returns a [WorkspaceEvent](WorkspaceEvent.md).

## Version

Introduced in version March 2015  

