# GeometricRelationships.add Method

Parent Object: [GeometricRelationships](GeometricRelationships.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a GeometricRelationship object, which defines two entities that will be used to either infer a joint or to create an assembly constraint.

## Syntax

"geometricRelationships_var" is a variable referencing a [GeometricRelationships](GeometricRelationships.md) object.

```python
# Uses no optional arguments.
returnValue = geometricRelationships_var.add(entityOne, entityTwo, isMate, value)

# Uses optional arguments.
returnValue = geometricRelationships_var.add(entityOne, entityTwo, isMate, value, biasPointOne, biasPointTwo)
```

## Return Value

| Type | Description |
|----|----|
| [GeometricRelationship](GeometricRelationship.md) | Returns the GeometricRelationship object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| entityOne | [Base](Base.md) | Specifies the entity from the first occurrence being constrained. The entity can be a BRepFace, BRepEdge, BRepVertex ,SketchLine, SketchPoint, ConstructionPlane, ConstructionAxis, or ConstructionPoint object in the component referenced by the occurrence. It must be a proxy relative to the root component of the assembly. For an inferred joint, if multiple geometric relationships are created, the entities for entityOne must all be from the same occurrence.This is because a single joint will be inferred between the two occurrences. For an assembly constraint, if multiple geometric relationships are created, the entities for entityOne must all be from the same occurrence. This is because all the geometric relationships constrain the occurrence this entity is from. |
| entityTwo | [Base](Base.md) | Specifies the entity from the second occurrence being constrained. The entity can be a BRepFace, BRepEdge, BRepVertex, SketchLine, SketchPoint, ConstructionPlane, ConstructionAxis, or ConstructionPoint object in the component referenced by the occurrence. It must be a proxy relative to the root component of the assembly. For an inferred joint, if multiple geometric relationships are created, the entities for entityTwo must all be from the same occurrence. This is because a single joint will be inferred between the two occurrences. For an assembly constraint, if multiple geometric relationships are created, the entities for entityTwo must all be from the same occurrence. This is because all the geometric relationships constrain the occurrence this entity is from. |
| isMate | boolean | Specifies if this geometric relationship defines a mate or an angle between the two input entities. If true, it defines a mate; if false, it is an angle. |
| value | [ValueInput](ValueInput.md) | Specifies the value associated with the geometric relationship. If isMate is true, the value is a length, and a real value in centimeters. If it is a string, it is an expression that must evaluate to a length. If the isMate argument is False, the value is an angle, and a real value in radians. If it is a string, it is an expression that must evaluate to an angle. |
| biasPointOne | [Point3D](Point3D.md) | This optional argument defines a position on the first entity that will be used when positioning the two occurrences. In the user interface, if you select two faces and create an inferred joint, the two faces will be used to mate the occurrences together. Still, there are infinite possibilities of how the occurrences can be positioned relative to one another. The location of the selection points is used to determine a single result, and the occurrences will be positioned so that the selection points are coincident. There aren't selection points in the API, but you can optionally define points that will be used, like the selection points. Fusion will calculate arbitrary points on the entities if the bias points aren't provided. The bias points are not remembered and are only used for the initial placement. This is an optional argument whose default value is null. |
| biasPointTwo | [Point3D](Point3D.md) | See the description for biasPointOne. This is an optional argument whose default value is null. |

## Version

Introduced in version July 2025  

