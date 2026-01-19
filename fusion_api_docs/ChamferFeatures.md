# ChamferFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing chamfer features in a component and supports the ability to create new chamfer features.

## Methods

| Name | Description |
|----|----|
| [add](ChamferFeatures_add.md) | Creates a new chamfer feature. |
| [classType](ChamferFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](ChamferFeatures_createInput.md) | \*\*RETIRED\*\* Creates a ChamferFeatureInput object. Use properties and methods on this object to define the chamfer you want to create and then use the Add method, passing in the ChamferFeatureInput object. |
| [createInput2](ChamferFeatures_createInput2.md) | Creates a ChamferFeatureInput object. Use properties and methods on this object to define the chamfer you want to create and then use the Add method, passing in the ChamferFeatureInput object. |
| [item](ChamferFeatures_item.md) | Function that returns the specified chamfer feature using an index into the collection. |
| [itemByName](ChamferFeatures_itemByName.md) | Function that returns the specified chamfer feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](ChamferFeatures_count.md) | The number of chamfer features in the collection. |
| [isValid](ChamferFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ChamferFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.chamferFeatures](Features_chamferFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Equal Distance Chamfer Feature API Sample](EqualDistanceChamferFeature_Sample.md) | Creates an equal distance chamfer on the selected edge. If there are tangent contiguous edges that will also be included in the chamfer. |

## Version

Introduced in version November 2014  

