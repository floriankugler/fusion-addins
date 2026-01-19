# FilletFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a fillet feature.

## Methods

| Name | Description |
|----|----|
| [addChordLengthEdgeSet](FilletFeatureInput_addChordLengthEdgeSet.md) | \*\*RETIRED\*\* Adds a set of edges with a chord length to this input. |
| [addConstantRadiusEdgeSet](FilletFeatureInput_addConstantRadiusEdgeSet.md) | \*\*RETIRED\*\* Adds a set of edges with a constant radius to this input. |
| [addVariableRadiusEdgeSet](FilletFeatureInput_addVariableRadiusEdgeSet.md) | \*\*RETIRED\*\* Adds a single edge or set of tangent edges along with variable radius information to this input. |
| [classType](FilletFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [edgeSetInputs](FilletFeatureInput_edgeSetInputs.md) | Gets the FilletEdgeSetInputs object that provides support to create the various types of edge sets that will be used to create the fillet. |
| [isG2](FilletFeatureInput_isG2.md) | **RETIRED** Gets and sets if the fillet uses the G2 (curvature-continuity) surface quality option. |
| [isRollingBallCorner](FilletFeatureInput_isRollingBallCorner.md) | Gets and sets if a rolling ball or setback solution is to be used in any corners. For an asymmetric fillet only a setback solution is supported, so any asymmetric edge sets will ignore this setting and will always be a setback corner. |
| [isTangentChain](FilletFeatureInput_isTangentChain.md) | **RETIRED** Gets and sets if any edges that are tangentially connected to any of filleted edges will also be included in the fillet. |
| [isValid](FilletFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FilletFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [targetBaseFeature](FilletFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[FilletFeatures.createInput](FilletFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Fillet Feature API Sample](FilletFeatureSample_Sample.md) | Demonstrates creating fillets using the various types of fillets. Create a new design and add a box that is at least 2 cm on each side. The script creates a constant radius, variable radius and chord length fillets. After creating each one, it deletes it and then creates the next. To see any of the fillets that were deleted, undo to get the fillet back. |

## Version

Introduced in version November 2014  

