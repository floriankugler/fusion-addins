# PatchFeature Object

Derived from: [Feature](Feature.md) Object  

## Description

An object that represents an existing patch feature in a design.

## Methods

| Name | Description |
| --- | --- |
| [classType](PatchFeature_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](PatchFeature_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e., a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](PatchFeature_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](PatchFeature_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |
| [getContinuity](PatchFeature_getContinuity.md) | Gets the continuity used for each edge in the boundary. To call this method, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [setContinuity](PatchFeature_setContinuity.md) | Sets the continuity to use for each edge in the boundary. The arrays for the arguments correspond to B-Rep edges in the boundary. You can use the getContinuity method to get the list of edges to know their order. This order applies to the arrays provided for the arguments. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](PatchFeature_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](PatchFeature_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](PatchFeature_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bodies](PatchFeature_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [boundaryCurve](PatchFeature_boundaryCurve.md) | Returns an ObjectCollection that contains all of the sketch curves or B-Rep edges that defines the closed outer boundary of the patch feature. When setting this property, the input can be a sketch profile, a single sketch curve, a single B-Rep edge, or an ObjectCollection of sketch curves and B-Rep edges. If a single open sketch curve or B-Rep edge is input, Fusion will automatically find connected sketch curves or B-Rep edges to define a closed loop. If an ObjectCollection of sketch curves or B-Rep edges is input, they must define a closed shape. To get or set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [continuity](PatchFeature_continuity.md) | **RETIRED** Gets and sets the type of surface continuity used when creating the patch face. This value is only used when BRepEdges are input and defines the continuity of how the patch face connects to the face adjacent to each of the input edges. To set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [entityToken](PatchFeature_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](PatchFeature_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [faces](PatchFeature_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [groupContinuity](PatchFeature_groupContinuity.md) | Gets and sets the type of surface continuity to use for all edges when the isGroupEdges property is true. The continuity is used to determine how the patch connects to any B-Rep edges in the boundary. It is ignored for any sketch curves in the boundary. The property defaults to ConnectedSurfaceContinuityType. The value of this property is ignored if the isGroupEdges property is false. To get or set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [groupIsContinuityDirectionFlipped](PatchFeature_groupIsContinuityDirectionFlipped.md) | Gets and sets the continuity direction for all edges when the isGroupEdges property is true. It is ignored for any sketch curves in the boundary. The property defaults to false. The value of this property is ignored if the isGroupEdges property is false. To get or set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [groupWeight](PatchFeature_groupWeight.md) | Gets and sets the weight to use for all edges when the isGroupEdges property is true. It is ignored for any sketch curves in the boundary. The property defaults to 0.5. The value of this property is ignored if the isGroupEdges property is false. To get or set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [healthState](PatchFeature_healthState.md) | Returns the current health state of the feature. |
| [interiorRailsAndPoints](PatchFeature_interiorRailsAndPoints.md) | Gets and sets any interior curves or points the patch should fit through. Valid entities include object collections of connected curves, paths, sketch curves, sketch points, B-Rep edges, and construction points. When getting this property, the returned ObjectCollection can contain individual edges, sketch curves, sketch points, construction points, vertices, and ObjectCollection objects that represent a group of the curves and points listed above. Can be set to null to remove any interior rails and points from the patch. To get or set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isGroupEdges](PatchFeature_isGroupEdges.md) | Gets and sets if the edges in the boundary curve are treated as a group , and they all use the same continuity. If this property is True (which is the default), the continuity for all edges is controlled by the continuity property. If this property is false; the continuity is set for each edge using the setContinuity method. When this property is set to true, the continuity and weight of the first edge will be used for all edges. When set to false, each edge will initially have the same continuity and weight. This property is typically set to false by calling the setContinuity method, which has the side effect of changing this to false. To get or set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isParametric](PatchFeature_isParametric.md) | Indicates if this feature is parametric or not. |
| [isSuppressed](PatchFeature_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isValid](PatchFeature_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](PatchFeature_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [name](PatchFeature_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [nativeObject](PatchFeature_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](PatchFeature_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](PatchFeature_operation.md) | Gets the type of operation performed by the patch feature. |
| [parentComponent](PatchFeature_parentComponent.md) | Returns the parent component that owns this feature. |
| [timelineObject](PatchFeature_timelineObject.md) | Returns the timeline object associated with this feature. |

## Accessed From

[PatchFeature.createForAssemblyContext](PatchFeature_createForAssemblyContext.md), [PatchFeature.nativeObject](PatchFeature_nativeObject.md), [PatchFeatures.add](PatchFeatures_add.md), [PatchFeatures.item](PatchFeatures_item.md), [PatchFeatures.itemByName](PatchFeatures_itemByName.md)

## Samples

| Name | Description |
|----|----|
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version September 2015  

