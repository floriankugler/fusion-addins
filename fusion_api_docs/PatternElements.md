# PatternElements Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to pattern elements of mirror and pattern features.

## Methods

| Name | Description |
|----|----|
| [classType](PatternElements_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](PatternElements_item.md) | Function that returns the specified pattern element using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](PatternElements_count.md) | The number of pattern elements in the collection. |
| [isValid](PatternElements_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PatternElements_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CircularPatternFeature.patternElements](CircularPatternFeature_patternElements.md), [MirrorFeature.patternElements](MirrorFeature_patternElements.md), [PathPatternFeature.patternElements](PathPatternFeature_patternElements.md), [RectangularPatternFeature.patternElements](RectangularPatternFeature_patternElements.md)

## Version

Introduced in version November 2014  

