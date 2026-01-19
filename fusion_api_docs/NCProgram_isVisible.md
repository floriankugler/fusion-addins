# NCProgram.isVisible Property

Parent Object: [NCProgram](NCProgram.md)  

## Description

Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children. This property indicates the final result and whether this operation is actually visible or not.

## Syntax

"nCProgram_var" is a variable referencing a NCProgram object.  

```python
# Get the value of the property.
propertyValue = nCProgram_var.isVisible
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version July 2023  

