# FilletEdgeSet Object

Derived from: [Base](Base.md) Object  

## Description

The base class for the classes that define the different types of fillet edge sets.

## Methods

| Name | Description |
| --- | --- |
| [classType](FilletEdgeSet_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](FilletEdgeSet_deleteMe.md) | Deletes the fillet edge set from the fillet. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |

## Properties

| Name | Description |
| --- | --- |
| [continuity](FilletEdgeSet_continuity.md) | Gets and sets the continuity of the fillet edge set. Valid values are TangentSurfaceContinuityType and CurvatureSurfaceContinuityType. |
| [isTangentChain](FilletEdgeSet_isTangentChain.md) | Gets and sets the Tangent chain for fillet. This enables tangent chain option for fillet. |
| [isValid](FilletEdgeSet_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FilletEdgeSet_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [tangencyWeight](FilletEdgeSet_tangencyWeight.md) | Returns the model parameter that controls the G1 or G2 tangency weight of the fillet. It must be a real value between 0.1 and 2.0 inclusive. You can edit the tangency weight by using the properties on the returned ModelParameter object. |

## Accessed From

[FilletEdgeSets.item](FilletEdgeSets_item.md)

## Derived Classes

[AsymmetricFilletEdgeSet](AsymmetricFilletEdgeSet.md), [ChordLengthFilletEdgeSet](ChordLengthFilletEdgeSet.md), [ConstantRadiusFilletEdgeSet](ConstantRadiusFilletEdgeSet.md), [VariableRadiusFilletEdgeSet](VariableRadiusFilletEdgeSet.md)

## Version

Introduced in version November 2014  

