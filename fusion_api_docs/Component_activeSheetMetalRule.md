# Component.activeSheetMetalRule Property

Parent Object: [Component](Component.md)  

## Description

Gets and sets the active sheet metal rule. This can return null in the case where the component has never contained any sheet metal related data.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.activeSheetMetalRule

# Set the value of the property.
component_var.activeSheetMetalRule = propertyValue
```

## Property Value

This is a read/write property whose value is a [SheetMetalRule](SheetMetalRule.md).

## Version

Introduced in version November 2022  

