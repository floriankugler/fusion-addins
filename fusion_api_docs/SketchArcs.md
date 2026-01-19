# SketchArcs Object

Derived from: [Base](Base.md) Object  

## Description

The collection of arcs in a sketch. This provides access to the existing arcs and supports the methods to create new arcs.

## Methods

| Name | Description |
|----|----|
| [addByCenterStartEnd](SketchArcs_addByCenterStartEnd.md) | Creates a sketch arc that is centered at the specified point and between the two input points. |
| [addByCenterStartSweep](SketchArcs_addByCenterStartSweep.md) | Creates a sketch arc that is always parallel to the x-y plane of the sketch and is centered at the specified point. |
| [addByThreePoints](SketchArcs_addByThreePoints.md) | Creates a sketch arc that passes through the three points. |
| [addFillet](SketchArcs_addFillet.md) | Creates a fillet between two sketch entities The side (quadrant) the fillet is created on is determined by the points specified. The point for each entity can be its startSketchPoint or endSketchPoint |
| [classType](SketchArcs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchArcs_item.md) | Function that returns the specified sketch arc using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchArcs_count.md) | Returns the number of arcs in the sketch. |
| [isValid](SketchArcs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchArcs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[SketchCurves.sketchArcs](SketchCurves_sketchArcs.md)

## Samples

| Name | Description |
|----|----|
| [SketchArcs.addByCenterStartSweep](SketchArcs_addByCenterStartaSweep_Sample.md) | Demonstrates the SketchArcs.addByCenterStartSweep method. |
| [SketchArcs.addByThreePoints](SketchArcs_addByThreePoints_Sample.md) | Demonstrates the SketchArcs.addByThreePoints method. |
| [SketchArcs.addFillet](SketchArcs_addFillet_Sample.md) | Demonstrates the SketchArcs.addFillet method. |
| [SketchArcs.breakCurve](SketchArcs_breakCurve_Sample.md) | Demonstrates the SketchArc.breakCurve method. |
| [SketchArcs.extend](SketchArcs_extend_Sample.md) | Demonstrates the SketchArc.extend method. |
| [SketchArcs.split](SketchArcs_split_Sample.md) | Demonstrates the SketchArc.split method. |
| [Sketch fillet and offset API Sample](SketchFilletAndOffset_Sample.md) | Demonstrates the creation of a fillet in a sketch and offset a set of curves. |

## Version

Introduced in version August 2014  

