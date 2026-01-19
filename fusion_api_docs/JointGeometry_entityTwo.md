# JointGeometry.entityTwo Property

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

This is the second entity that defines this joint geometry. This isn't used for all joint geometry types and will return null in the cases where it's not used. A second geometry is used in the case where the geometryType property returns JointProfileGeometry, JointPlanarBRepFaceGeometry, JointBetweenTwoFacesGeometry or JointByTwoEdgeIntersectionGeometry.

## Syntax

"jointGeometry_var" is a variable referencing a JointGeometry object.  

```python
# Get the value of the property.
propertyValue = jointGeometry_var.entityTwo
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version July 2015  

