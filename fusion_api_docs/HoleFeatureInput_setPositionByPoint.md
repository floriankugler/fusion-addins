# HoleFeatureInput.setPositionByPoint Method

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Defines the position of a the hole using a point. The point can be a vertex on the face or it can be a Point3D object to define any location on the face. If a Point3D object is provided it will be projected onto the plane along the planes normal. The orientation of the hole is defined by the planar face or construction plane. If a vertex is used, the position of the hole is associative to that vertex. If a Point3D object is used the position of the hole is not associative.

## Syntax

"holeFeatureInput_var" is a variable referencing a [HoleFeatureInput](HoleFeatureInput.md) object.

```python
returnValue = holeFeatureInput_var.setPositionByPoint(planarEntity, point)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntity | [Base](Base.md) | The planar BRepFace or ConstructionPlane object that defines the orientation of the hole. The natural direction of the hole will be opposite the normal of the face or construction plane. |
| point | [Base](Base.md) | A Point3D object or vertex that defines the position of the hole. The point will be projected onto the plane along the normal of the plane. |

## Version

Introduced in version August 2014  

