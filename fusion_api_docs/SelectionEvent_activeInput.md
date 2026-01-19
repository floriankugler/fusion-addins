# SelectionEvent.activeInput Property

Parent Object: [SelectionEvent](SelectionEvent.md)  

## Description

Returns the SelectionCommandInput that is currently active in the command dialog and that the user is selecting entities for. This can be used to determine which set of rules you want to apply to determine if the current entity is selectable or not.

## Syntax

"selectionEvent_var" is a variable referencing a SelectionEvent object.  

```python
# Get the value of the property.
propertyValue = selectionEvent_var.activeInput
```

## Property Value

This is a read only property whose value is a [SelectionCommandInput](SelectionCommandInput.md).

## Version

Introduced in version July 2015  

