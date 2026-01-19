# HoleFeature.setPositionAtCenter Method

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Redefines the position of the hole at the center of a circular or elliptical edge of the face.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"holeFeature_var" is a variable referencing a [HoleFeature](HoleFeature.md) object.

```python
returnValue = holeFeature_var.setPositionAtCenter(planarEntity, centerEdge)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntity | [Base](Base.md) | The planar BRepFace or ConstructionPlane object that defines the orientation of the hole. The natural direction of the hole will be opposite the normal of the face or construction plane. |
| centerEdge | [BRepEdge](BRepEdge.md) | A circular or elliptical edge whose center point will be the position of the hole. |

## Version

Introduced in version August 2014  

