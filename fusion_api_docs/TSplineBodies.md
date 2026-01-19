# TSplineBodies Object

Derived from: [Base](Base.md) Object  

## Description

A collection of TSpline bodies.

## Methods

| Name | Description |
|----|----|
| [addByTSMDescription](TSplineBodies_addByTSMDescription.md) | Creates a new TSplineBody using the T-Spline description provided by the input string which contains TSM formatted text. |
| [addByTSMFile](TSplineBodies_addByTSMFile.md) | Creates a new TSplineBody by reading in a TSM file from disk. |
| [classType](TSplineBodies_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](TSplineBodies_item.md) | Function that returns the specified T-Spline body using an index into the collection. |
| [itemByName](TSplineBodies_itemByName.md) | Returns a TSplineBody by specifying the name of the body as seen in the browser. |

## Properties

| Name | Description |
| --- | --- |
| [count](TSplineBodies_count.md) | The number of bodies in the collection. |
| [isValid](TSplineBodies_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](TSplineBodies_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[FormFeature.tSplineBodies](FormFeature_tSplineBodies.md)

## Version

Introduced in version April 2019  

