# BRepBody.isVisible Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

Gets if this body is currently visible in the graphics window. Use the isLightBulbOn to change if the light bulb beside the body node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children. This property indicates the final result and whether this body is actually visible or not.  

This property is only valid if the IsTransient property is false.

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.isVisible

# Set the value of the property.
bRepBody_var.isVisible = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [BRep Body Sample](BRepBodySample_Sample.md) | B-Rep (Boundary Representation) body related functions |

## Version

Introduced in version August 2014  

