# Decal.redefine Method

Parent Object: [Decal](Decal.md)  

## Description

Redefines the position, orientation, and how the decal is applied to the body.  

To call this method, you need to position the timeline marker to immediately before this decal. This can be accomplished using the following code: thisDecal.timelineObject.rollTo(True)

## Syntax

"decal_var" is a variable referencing a [Decal](Decal.md) object.

```python
returnValue = decal_var.redefine(position, faces, isChainFaces)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| position | [Matrix3D](Matrix3D.md) | Defines the position, rotation, scaling, and flipping of the decal. The input 3D matrix defines a 3D coordinate system in model space. The origin of the matrix defines the center of the decal and must lie somewhere on the first face. The Z-axis of the matrix should be the same as the normal of the face at the origin. The X and Y axes define the orientation of the decal and must be both perpendicular to the Z axis and each other. Reversing the direction of the X or Y axis will flip the decal in that direction. The magnitude of the X and Y axes controls the scale, and the scale can be non-uniform, meaning the length of the X and Y vectors do not need to be the same. |
| faces | BRepFace\[\] | Defines the face where the decal will be placed. The first face in the array is the primary face, which is where the position point must be on. If the isChainFaces argument is true, only the primary face is needed and it will be used to define the position and orientation of the decal and the decal can wrap onto all the faces of the body. If the isChainFaces argument is false, the decal can only be applied to the specified faces with the first face in the array being used as the primary face. |
| isChainFaces | boolean | If true, only one face is needed and the decal wraps onto all the faces of the body. If false, the decal can only be applied to the specified faces with the first face being used to calculate the position and orientation. |

## Version

Introduced in version September 2024  

