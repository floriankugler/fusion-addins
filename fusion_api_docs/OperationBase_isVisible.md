# OperationBase.isVisible Property

Parent Object: [OperationBase](OperationBase.md)  

## Description

Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children. This property indicates the final result and whether this operation is actually visible or not.

## Syntax

"operationBase_var" is a variable referencing an OperationBase object.  

```python
# Get the value of the property.
propertyValue = operationBase_var.isVisible
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version July 2023  

