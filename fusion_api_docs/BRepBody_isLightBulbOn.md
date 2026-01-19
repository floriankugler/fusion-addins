# BRepBody.isLightBulbOn Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

Gets and set if the light bulb beside the body node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children so this property does not indicate if the body is actually visible, just that it should be visible if all of it's parent nodes are also visible. Use the isVisible property to determine if it's actually visible.  

This property is only valid if the IsTransient property is false.

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.isLightBulbOn

# Set the value of the property.
bRepBody_var.isLightBulbOn = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [BRep Body Sample](BRepBodySample_Sample.md) | B-Rep (Boundary Representation) body related functions |

## Version

Introduced in version January 2016  

