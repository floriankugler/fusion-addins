# SketchLines.addAngleChamfer Method

Parent Object: [SketchLines](SketchLines.md)  

## Description

Creates a chamfer between two sketch lines. In the case where the two input lines cross each other creating an "X" shape, this results in four quadrants where the chamfer can be placed. The point arguments are used to define which of the four quadrants the chamfer should be created in. The two points define which side of the two lines should be kept and the other end will be trimmed by the chamfer. The easiest way to use this is to use the end points of the lines on the side you want to keep. In the case where the lines don't intersect or connect at the end points, there is only one valid quadrant for the chamfer so the points are ignored.

## Syntax

"sketchLines_var" is a variable referencing a [SketchLines](SketchLines.md) object.

```python
returnValue = sketchLines_var.addAngleChamfer(firstLine, firstLinePoint, secondLine, secondLinePoint, distance, angle)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLine](SketchLine.md) | Returns the newly created SketchLine object that represents the chamfer or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| firstLine | [SketchLine](SketchLine.md) | The first line you want to chamfer. |
| firstLinePoint | [Point3D](Point3D.md) | A point on the first line that is on the side of the intersection with the second line that you want to keep. |
| secondLine | [SketchLine](SketchLine.md) | The second line you want to chamfer. |
| secondLinePoint | [Point3D](Point3D.md) | A point on the second line that is on the side of the intersection with the first line that you want to keep. |
| distance | double | Defines the distance of the start point of the chamfer from the intersection point of the two lines along the first line. The distance is defined in centimeters. |
| angle | double | Defines the angle of the chamfer as measured from the first line. The angle is defined in radians. |

## Samples

| Name | Description |
|----|----|
| [Sketch Chamfer API Sample](SketchChamferSample_Sample.md) | Demonstrates creating a new sketch point. |
| [SketchLines.addAngleChamfer](SketchLines_addAngleChamfer_Sample.md) | Demonstrates the SketchLines.addAngleChamfer method. |

## Version

Introduced in version March 2021  

