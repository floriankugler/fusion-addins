# SketchLineList Object

Derived from: [Base](Base.md) Object  

## Description

A list of sketch lines.

## Methods

| Name | Description |
|----|----|
| [classType](SketchLineList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchLineList_item.md) | Function that returns the specified sketch line using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchLineList_count.md) | Returns the number of sketch lines in the list. |
| [isValid](SketchLineList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchLineList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[SketchLines.addCenterPointRectangle](SketchLines_addCenterPointRectangle.md), [SketchLines.addEdgePolygon](SketchLines_addEdgePolygon.md), [SketchLines.addScribedPolygon](SketchLines_addScribedPolygon.md), [SketchLines.addThreePointRectangle](SketchLines_addThreePointRectangle.md), [SketchLines.addTwoPointRectangle](SketchLines_addTwoPointRectangle.md), [SketchText.boundaryLines](SketchText_boundaryLines.md)

## Version

Introduced in version August 2014  

