# ListControlDefinition.lastSelected Property

Parent Object: [ListControlDefinition](ListControlDefinition.md)  

## Description

Gets the item in the list that was last selected. This can return null in the case where this control is displayed as a list of check boxes and there hasn't been any interaction by the end-user. In the case of a list of check boxes, this returns the item that was last clicked by the user, whether it was to check or uncheck the item. In the case of a list of radio buttons, this always returns the item that is currently selected.

## Syntax

"listControlDefinition_var" is a variable referencing a ListControlDefinition object.  

```python
# Get the value of the property.
propertyValue = listControlDefinition_var.lastSelected
```

## Property Value

This is a read only property whose value is a [ListItem](ListItem.md).

## Version

Introduced in version August 2014  

