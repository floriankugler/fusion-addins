# DraftAnalyses Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to any draft analyses results in the design.

## Methods

| Name | Description |
|----|----|
| [classType](DraftAnalyses_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](DraftAnalyses_item.md) | A method that returns the specified DraftAnalysis object using an index into the collection. |
| [itemByName](DraftAnalyses_itemByName.md) | A method that returns the specified DraftAnalysis object using the name of the analysis as displayed in the browser. |

## Properties

| Name | Description |
| --- | --- |
| [count](DraftAnalyses_count.md) | Returns the number of DraftAnalysis objects in the collection. |
| [isValid](DraftAnalyses_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DraftAnalyses_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Analyses.draftAnalyses](Analyses_draftAnalyses.md)

## Version

Introduced in version January 2023  

