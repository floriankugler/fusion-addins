# FilletEdgeSetInputs Object

Derived from: [Base](Base.md) Object  

## Description

Collection of edge sets associated with the input object that will be used to create the new fillet feature. Use the various add methods on this object to add new edge sets to the input object.

## Methods

| Name | Description |
|----|----|
| [addAsymmetricRadiusEdgeSet](FilletEdgeSetInputs_addAsymmetricRadiusEdgeSet.md) | Adds an asymmetric fillet edge set to the fillet feature input. Some settings are initialized with a default value and can be set by modifying properties on the returned AsymmetricFilletEdgeSetInput object. |
| [addChordLengthEdgeSet](FilletEdgeSetInputs_addChordLengthEdgeSet.md) | Adds a set of edges to be filleted with a chord length fillet to the fillet feature input. Some settings are initialized with a default value and can be set by modifying properties on the returned ChordLengthFilletEdgeSetInput object. |
| [addConstantRadiusEdgeSet](FilletEdgeSetInputs_addConstantRadiusEdgeSet.md) | Adds a constant radius fillet edge set to the fillet feature input. Some settings are initialized with a default value and can be set by modifying properties on the returned ConstantRadiusFilletEdgeSetInput object. |
| [addVariableRadiusEdgeSet](FilletEdgeSetInputs_addVariableRadiusEdgeSet.md) | Adds a single edge or set of tangent edges to the fillet feature input. Some settings are initialized with a default value and can be set by modifying properties on the returned VariableRadiusFilletEdgeSetInput object. |
| [classType](FilletEdgeSetInputs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](FilletEdgeSetInputs_item.md) | Function that returns the specified fillet edge set input using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](FilletEdgeSetInputs_count.md) | The number of fillet edge set input objects in the collection. |
| [isValid](FilletEdgeSetInputs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FilletEdgeSetInputs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[FilletFeatureInput.edgeSetInputs](FilletFeatureInput_edgeSetInputs.md)

## Samples

| Name | Description |
|----|----|
| [filletFeatures.add](filletFeatures_add_Sample.md) | Demonstrates the filletFeatures.add method. |
| [Fillet Feature API Sample](FilletFeatureSample_Sample.md) | Demonstrates creating fillets using the various types of fillets. Create a new design and add a box that is at least 2 cm on each side. The script creates a constant radius, variable radius and chord length fillets. After creating each one, it deletes it and then creates the next. To see any of the fillets that were deleted, undo to get the fillet back. |

## Version

Introduced in version November 2022  

