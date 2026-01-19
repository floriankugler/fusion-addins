# OperationBase.isLightBulbOn Property

Parent Object: [OperationBase](OperationBase.md)  

## Description

Gets if this operation is currently visible in the graphics window. Use the isLightBulbOn to change if the eye icon beside the operation node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children so this property does not indicate if the operation is actually visible, just that it should be visible if all of its parent nodes are also visible. Use the isVisible property to determine if it's actually visible.

## Syntax

"operationBase_var" is a variable referencing an OperationBase object.  

```python
# Get the value of the property.
propertyValue = operationBase_var.isLightBulbOn

# Set the value of the property.
operationBase_var.isLightBulbOn = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2023  

