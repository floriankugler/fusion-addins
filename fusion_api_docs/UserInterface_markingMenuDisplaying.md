# UserInterface.markingMenuDisplaying Event

Parent Object: [UserInterface](UserInterface.md)  

## Description

The markingMenuDisplaying event fires just before the marking menu and context menus are displayed. The marking menu is the round menu displayed when the user right-clicks the mouse within Fusion. The context menu is the vertical menu displayed. The event provides both the marking menu and the context menu so you can examine and edit the contents of either one or both of them before they are displayed. Fusion will then display the marking and context menu that you've customized. If either one is empty it will not be displayed.

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
# "MyMarkingMenuDisplayingHandler" is the name of the class that handles the event.
onMarkingMenuDisplaying = MyMarkingMenuDisplayingHandler()
userInterface_var.markingMenuDisplaying.add(onMarkingMenuDisplaying)
handlers.append(onMarkingMenuDisplaying)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the markingMenuDisplaying event.
class MyMarkingMenuDisplayingHandler(adsk.core.MarkingMenuEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.MarkingMenuEventArgs):
        # Code to react to the event.
        app.log('In MyMarkingMenuDisplayingHandler event handler.')
```

## Property Value

This is an event property that returns a [MarkingMenuEvent](MarkingMenuEvent.md).

## Samples

| Name | Description |
|----|----|
| [Marking Menu API Sample](MarkingMenuSample_Sample.md) | Demonstrates how to customize marking menu and context menu. This sample is an add-in. To use it, create a new add-in using the "Scrips and Add-Ins" command. Use any name you would like for the add-in. In the folder where the add-in was created edit the *add-in name*.py file and replace it's entire contents with the sample code below. You can also delete all the other files that were created for the add-in except for *add-in name*.manifiest. Start the add-in from the "Scripts and Add-Ins" dialog. Now, with the add-in running, whenever you right-click in the Fusion window, you'll get an entirely customized context menu. The default marking menu has been modified by the add-in by removing the existing commands and adding some custom commands. |

## Version

Introduced in version January 2017  

