# AsymmetricFilletEdgeSet Object

Derived from: [FilletEdgeSet](FilletEdgeSet.md) Object  

## Description

Provides access to the edges and the parameters associated with an asymmetric fillet.

## Methods

| Name | Description |
| --- | --- |
| [classType](AsymmetricFilletEdgeSet_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](AsymmetricFilletEdgeSet_deleteMe.md) | Deletes the fillet edge set from the fillet. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |

## Properties

| Name | Description |
| --- | --- |
| [continuity](AsymmetricFilletEdgeSet_continuity.md) | Gets and sets the continuity of the fillet edge set. Valid values are TangentSurfaceContinuityType and CurvatureSurfaceContinuityType. |
| [edges](AsymmetricFilletEdgeSet_edges.md) | Gets and sets an ObjectCollection containing the BRepEdge, BRepFace, and Feature that are filleted. If the isTangentChain argument is true additional edges or faces may also get filleted if they are tangentially connected to any of the input edges or faces. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isFlipped](AsymmetricFilletEdgeSet_isFlipped.md) | Gets and sets if offsets are reversed. If false, offsetOne is applied to the first direction and offsetTwo to the second direction. Setting to true reverses this. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isTangentChain](AsymmetricFilletEdgeSet_isTangentChain.md) | Gets and sets the Tangent chain for fillet. This enables tangent chain option for fillet. |
| [isValid](AsymmetricFilletEdgeSet_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](AsymmetricFilletEdgeSet_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offsetOne](AsymmetricFilletEdgeSet_offsetOne.md) | Returns the model parameter that controls the offset distance of the fillet in the first direction You can edit the offset by using the properties on the returned ModelParameter object. |
| [offsetTwo](AsymmetricFilletEdgeSet_offsetTwo.md) | Returns the model parameter that controls the offset distance of the fillet in the second direction You can edit the offset by using the properties on the returned ModelParameter object. |
| [tangencyWeight](AsymmetricFilletEdgeSet_tangencyWeight.md) | Returns the model parameter that controls the G1 or G2 tangency weight of the fillet. It must be a real value between 0.1 and 2.0 inclusive. You can edit the tangency weight by using the properties on the returned ModelParameter object. |

## Accessed From

[FilletEdgeSets.addAsymmetricRadiusEdgeSet](FilletEdgeSets_addAsymmetricRadiusEdgeSet.md)

## Version

Introduced in version November 2025  

