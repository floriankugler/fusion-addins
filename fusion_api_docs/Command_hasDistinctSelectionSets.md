# Command.hasDistinctSelectionSets Property

Parent Object: [Command](Command.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Determines if this selection input shares a common selection set with the other selection inputs of this command or its own unique selection set. The default is False, which means each selection input will have its own selection set. This means that the items in this selection set are only shown as selected when this selection input is active. As a result, other selection inputs associated with this command can select those same entities.  

If this is True, then all selection inputs share a selection set, which means that when entities are selected by any of the selection inputs of this command, they will remain selected regardless of which command input is active. This has the side effect that once an entity is selected, it cannot be selected again by another selection input.

## Syntax

"command_var" is a variable referencing a Command object.  

```python
# Get the value of the property.
propertyValue = command_var.hasDistinctSelectionSets

# Set the value of the property.
command_var.hasDistinctSelectionSets = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2024  

