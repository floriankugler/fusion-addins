# CustomGraphicsBRepBody.depthPriority Property

Parent Object: [CustomGraphicsBRepBody](CustomGraphicsBRepBody.md)  

## Description

Gets and sets the depth priority associated with the graphics entity. The depth priority defines how one graphics entity will be drawn with respect to another entity. This is useful when there are entities that lie in the same space so it's ambiguous which should be drawn on the other. For example, if you draw a curve on a planar mesh and want the curve to be completely visible. You can set the depth priority of the curve to be greater than the mesh so it will be drawn after the mesh and will remain visible.  

When a new graphics entity is created it's default depth priority is 0.

## Syntax

"customGraphicsBRepBody_var" is a variable referencing a CustomGraphicsBRepBody object.  

```python
# Get the value of the property.
propertyValue = customGraphicsBRepBody_var.depthPriority

# Set the value of the property.
customGraphicsBRepBody_var.depthPriority = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version September 2017  

