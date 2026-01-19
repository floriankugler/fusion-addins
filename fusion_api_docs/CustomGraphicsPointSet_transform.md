# CustomGraphicsPointSet.transform Property

Parent Object: [CustomGraphicsPointSet](CustomGraphicsPointSet.md)  

## Description

Gets and sets the transform associated with the graphics entity. When a new graphics entity is created its default transform is an identity matrix which results in the graphics entity being displayed in model space using the original coordinate data used to define the entity.

## Syntax

"customGraphicsPointSet_var" is a variable referencing a CustomGraphicsPointSet object.  

```python
# Get the value of the property.
propertyValue = customGraphicsPointSet_var.transform

# Set the value of the property.
customGraphicsPointSet_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version September 2017  

