# GeometricRelationship.angleReferenceEntity Property

Parent Object: [GeometricRelationship](GeometricRelationship.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

This property is used to define a third vector when an angle constraint is being defined. This property is ignored for mate constraints.  

In some cases, when specifying entityOne and entityTwo for an angle constraint there is more than one solution. When the constraint is solved, entityOne and entityTwo each define a vector. When the reference entity is provided, the vectors need to follow the "right hand rule" with respect to the reference entity. This means the angle between the reference entity and the cross product of entityOne and entityTwo should be between 0 and 90 deg.  

The reference entity can be a planar BRepFace or a linear or circular BRepedge.  

This property can return and be set to null to indicate there is no reference entity.

## Syntax

"geometricRelationship_var" is a variable referencing a GeometricRelationship object.  

```python
# Get the value of the property.
propertyValue = geometricRelationship_var.angleReferenceEntity

# Set the value of the property.
geometricRelationship_var.angleReferenceEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2025  

