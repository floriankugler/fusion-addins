# SketchLines Object

Derived from: [Base](Base.md) Object  

## Description

The collection of lines in a sketch. This provides access to the existing lines and supports the methods to create new lines.

## Methods

| Name | Description |
|----|----|
| [addAngleChamfer](SketchLines_addAngleChamfer.md) | Creates a chamfer between two sketch lines. In the case where the two input lines cross each other creating an "X" shape, this results in four quadrants where the chamfer can be placed. The point arguments are used to define which of the four quadrants the chamfer should be created in. The two points define which side of the two lines should be kept and the other end will be trimmed by the chamfer. The easiest way to use this is to use the end points of the lines on the side you want to keep. In the case where the lines don't intersect or connect at the end points, there is only one valid quadrant for the chamfer so the points are ignored. |
| [addByMidpoint](SketchLines_addByMidpoint.md) | Creates a sketch line where the first point is the midpoint and the second point is one endpoint. The system automatically calculates the other endpoint to create a line where the first point is exactly at the midpoint. |
| [addByTwoPoints](SketchLines_addByTwoPoints.md) | Creates a sketch line between the two input points. The input points can be either existing SketchPoints or Point3D objects. If a SketchPoint is used the new line will be based on that sketch point and update if the sketch point is modified. |
| [addCenterPointRectangle](SketchLines_addCenterPointRectangle.md) | Creates four sketch lines representing a rectangle where the first point represents the center of the rectangle. The second point is the corner of the rectangle and can be either an existing SketchPoint or Point3D object. The four sketch lines are returned. |
| [addDistanceChamfer](SketchLines_addDistanceChamfer.md) | Creates a chamfer between two sketch lines. In the case where the two input lines cross each other creating an "X" shape, this results in four quadrants where the chamfer can be placed. The point arguments are used to define which of the four quadrants the chamfer should be created in. The two points define which side of the two lines should be kept and the other end will be trimmed by the chamfer. The easiest way to use this is to use the end points of the lines on the side you want to keep. In the case where the lines don't intersect or connect at the end points, there is only one valid quadrant for the chamfer so the points are ignored. |
| [addEdgePolygon](SketchLines_addEdgePolygon.md) | Creates a polygon where two points specify an edge of the polygon. By specifying an edge, the size and position of the polygon is also defined. |
| [addScribedPolygon](SketchLines_addScribedPolygon.md) | Creates either an inscribed or circumscribed n-sided polygon. |
| [addThreePointRectangle](SketchLines_addThreePointRectangle.md) | Creates four sketch lines representing a rectangle where the first two points are the base corners of the rectangle and the third point defines the height. |
| [addTwoPointRectangle](SketchLines_addTwoPointRectangle.md) | Creates four sketch lines representing a rectangle where the two points are the opposing corners of the rectangle. The input points can be either existing SketchPoints or Point3D objects. If a SketchPoint is used the new lines will be based on that sketch point and update if the sketch point is modified. |
| [classType](SketchLines_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchLines_item.md) | Function that returns the specified sketch line using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchLines_count.md) | Returns the number of lines in the sketch. |
| [isValid](SketchLines_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchLines_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[SketchCurves.sketchLines](SketchCurves_sketchLines.md)

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |
| [SketchLines.addAngleChamfer](SketchLines_addAngleChamfer_Sample.md) | Demonstrates the SketchLines.addAngleChamfer method. |
| [SketchLines.addByTwoPoints](SketchLines_addByTwoPoints_Sample.md) | Demonstrates the SketchLines.addByTwoPoints method. |
| [SketchLines.addCenterPointRectangle](SketchLines_addCenterPointRectangle_Sample.md) | Demonstrates the SketchLines.addCenterPointRectangle method. |
| [SketchLines.addDistanceChamfer](SketchLines_addDistanceChamfer_Sample.md) | Demonstrates the SketchLines.addDistanceChamfer method. |
| [SketchLines.addThreePointRectangle](SketchLines_addThreePointRectangle_Sample.md) | Demonstrates the SketchLines.addThreePointRectangle method. |
| [SketchLines.addTwoPointRectangle](SketchLines_addTwoPointRectangle_Sample.md) | Demonstrates the SketchLines.addTwoPointRectangle method. |

## Version

Introduced in version August 2014  

