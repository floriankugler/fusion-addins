# ActiveSelectionEventArgs.currentSelection Property

Parent Object: [ActiveSelectionEventArgs](ActiveSelectionEventArgs.md)  

## Description

The list of all of the current selections. This is the same set of selections accessed through the UserInterface.activeSelection object. An empty array can be returned in the case where the selection has been cleared which can occur by the user unselecting and entity, terminating the select command pressing Escape or running another command or clicking the mouse in an open area of the canvas.

## Syntax

"activeSelectionEventArgs_var" is a variable referencing an ActiveSelectionEventArgs object.  

```python
# Get the value of the property.
propertyValue = activeSelectionEventArgs_var.currentSelection
```

## Property Value

This is a read only property whose value is an array of type [Selection](Selection.md).

## Version

Introduced in version August 2020  

