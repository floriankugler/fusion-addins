# ChamferFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a chamfer feature.

## Methods

| Name | Description |
|----|----|
| [classType](ChamferFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setToDistanceAndAngle](ChamferFeatureInput_setToDistanceAndAngle.md) | \*\*RETIRED\*\* Adds a set of edges to this input. |
| [setToEqualDistance](ChamferFeatureInput_setToEqualDistance.md) | \*\*RETIRED\*\* Adds a set of edges to this input. |
| [setToTwoDistances](ChamferFeatureInput_setToTwoDistances.md) | \*\*RETIRED\*\* Adds a set of edges to this input. |

## Properties

| Name | Description |
| --- | --- |
| [chamferEdgeSets](ChamferFeatureInput_chamferEdgeSets.md) | Returns the collection of edge sets for this chamfer feature input. |
| [cornerType](ChamferFeatureInput_cornerType.md) | Gets and sets the type of corner to be modeled when multiple edges connect at a vertex. |
| [edges](ChamferFeatureInput_edges.md) | **RETIRED** Gets and sets the collection of edges that will be chamfered. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isTangentChain](ChamferFeatureInput_isTangentChain.md) | **RETIRED** Gets and sets if any edges that are tangentially connected to any of chamfered edges will also be included in the chamfer. |
| [isValid](ChamferFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ChamferFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [targetBaseFeature](ChamferFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[ChamferFeatures.createInput](ChamferFeatures_createInput.md), [ChamferFeatures.createInput2](ChamferFeatures_createInput2.md)

## Samples

| Name | Description |
|----|----|
| [Equal Distance Chamfer Feature API Sample](EqualDistanceChamferFeature_Sample.md) | Creates an equal distance chamfer on the selected edge. If there are tangent contiguous edges that will also be included in the chamfer. |

## Version

Introduced in version November 2014  

