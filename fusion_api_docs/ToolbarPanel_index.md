# ToolbarPanel.index Property

Parent Object: [ToolbarPanel](ToolbarPanel.md)  

## Description

Gets the position this panel is in within the toolbar. The first panel is at position 0. This value is with respect to the complete list of panels so this value could be outside of the expected range if you have a collection of panels associated with a workspace, which is a subset of the entire list of panels.

## Syntax

"toolbarPanel_var" is a variable referencing a ToolbarPanel object.  

```python
# Get the value of the property.
propertyValue = toolbarPanel_var.index
```

## Property Value

This is a read only property whose value is a uinteger.

## Version

Introduced in version August 2014  

