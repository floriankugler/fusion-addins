# InterferenceResults Object

Derived from: [Base](Base.md) Object  

## Description

Transient object used to return the result of an interference analysis.

## Methods

| Name | Description |
|----|----|
| [classType](InterferenceResults_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createBodies](InterferenceResults_createBodies.md) | Creates bodies in the model that represent the interference volumes. This is not supported in parametric modeling. |
| [item](InterferenceResults_item.md) | Function that returns the specified interference result using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](InterferenceResults_count.md) | Returns the number of interference results in the collection. |
| [isValid](InterferenceResults_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](InterferenceResults_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Design.analyzeInterference](Design_analyzeInterference.md), [FlatPatternProduct.analyzeInterference](FlatPatternProduct_analyzeInterference.md), [WorkingModel.analyzeInterference](WorkingModel_analyzeInterference.md)

## Samples

| Name | Description |
|----|----|
| [Interference API Sample](InterferenceSample_Sample.md) | Demonstrates Interference APIs. |

## Version

Introduced in version November 2015  

