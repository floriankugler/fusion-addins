# GeometricRelationship.entityOne Property

Parent Object: [GeometricRelationship](GeometricRelationship.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the first entity in the relationship. The entity can be a BRepFace, BRepedge, BRepVertex, SketchPoint, SketchCurve, ConstructionPlane, ConstructionAxis, or ConstructionPoint object.  

If the GeometricRelationship is associated with an existing joint or assembly constraint (the isTemporary property is false), you need to position the timeline marker immediately before the joint or assembly constraint. This can be accomplished using the following code: thisJointOrConstraint.timelineObject.rollTo(True).

## Syntax

"geometricRelationship_var" is a variable referencing a GeometricRelationship object.  

```python
# Get the value of the property.
propertyValue = geometricRelationship_var.entityOne

# Set the value of the property.
geometricRelationship_var.entityOne = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2025  

