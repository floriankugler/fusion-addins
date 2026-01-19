# TwoDistancesChamferEdgeSet Object

Derived from: [ChamferEdgeSet](ChamferEdgeSet.md) Object  

## Description

Provides access to the edges and the parameters associated with a two distances chamfer.

## Methods

| Name | Description |
| --- | --- |
| [classType](TwoDistancesChamferEdgeSet_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](TwoDistancesChamferEdgeSet_deleteMe.md) | Deletes the chamfer edge set from the chamfer. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |

## Properties

| Name | Description |
| --- | --- |
| [distanceOne](TwoDistancesChamferEdgeSet_distanceOne.md) | Returns the model parameter that controls the first offset distance of the chamfer. You can edit the distance by using the properties on the returned ModelParameter object. |
| [distanceTwo](TwoDistancesChamferEdgeSet_distanceTwo.md) | Returns the model parameter that controls the first offset distance of the chamfer. You can edit the distance by using the properties on the returned ModelParameter object. |
| [edges](TwoDistancesChamferEdgeSet_edges.md) | Gets and sets the edges that will be chamfered. This collection can contain BRepEdge, BRepFace, and Feature objects. If BRepFace or Feature are objects are provided, all of the edges associated with those objects will be chamfered. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isFlipped](TwoDistancesChamferEdgeSet_isFlipped.md) | Gets and sets if the chamfer is flipped. This swaps the directions for distance one and two. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isTangentChain](TwoDistancesChamferEdgeSet_isTangentChain.md) | Gets and sets the Tangent chain for chamfer. This enables tangent chain option for chamfer. |
| [isValid](TwoDistancesChamferEdgeSet_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](TwoDistancesChamferEdgeSet_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version December 2020  

