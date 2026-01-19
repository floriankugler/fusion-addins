# ToolbarTab.index Property

Parent Object: [ToolbarTab](ToolbarTab.md)  

## Description

Gets the position this tab is in within the toolbar. The first tab is at position 0. This value is with respect to the complete list of tabs so this value could be outside of the expected range if you have a collection of tabs associated with a workspace, which is a subset of the entire list of tabs.

## Syntax

"toolbarTab_var" is a variable referencing a ToolbarTab object.  

```python
# Get the value of the property.
propertyValue = toolbarTab_var.index
```

## Property Value

This is a read only property whose value is a uinteger.

## Version

Introduced in version August 2019  

