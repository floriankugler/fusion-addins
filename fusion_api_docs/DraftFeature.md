# DraftFeature Object

Derived from: [Feature](Feature.md) Object  

## Description

Object that represents an existing draft feature in a design.

## Methods

| Name | Description |
| --- | --- |
| [classType](DraftFeature_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](DraftFeature_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](DraftFeature_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](DraftFeature_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |
| [setSingleAngle](DraftFeature_setSingleAngle.md) | Changes the definition of the feature so that a single angle is used for all drafts. If the isSymmetric is true then the faces are split along the parting plane and drafted independently using the same angle. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [setTwoAngles](DraftFeature_setTwoAngles.md) | Changes the definition of the feature so that the surfaces are split along the draft plane or parting line and the faces on each side of the plane are drafted independently. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](DraftFeature_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](DraftFeature_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](DraftFeature_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bodies](DraftFeature_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [draftDefinition](DraftFeature_draftDefinition.md) | Gets the definition object that specifies how the draft is defined. Modifying the definition object will cause the draft to recompute. This can return either an AngleExtentDefinition or TwoSidesAngleExtentDefinition object. This property returns nothing in the case where the feature is non-parametric. Use this property to access the parameters controlling the draft and whether the draft is symmetric or not. |
| [entityToken](DraftFeature_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](DraftFeature_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [faces](DraftFeature_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [healthState](DraftFeature_healthState.md) | Returns the current health state of the feature. |
| [inputFaces](DraftFeature_inputFaces.md) | Gets and sets the input faces. If isTangentChain is true, all the faces that are tangentially connected to the input faces (if any) will also be included. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isDirectionFlipped](DraftFeature_isDirectionFlipped.md) | Gets and sets if the direction of the draft is flipped. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isParametric](DraftFeature_isParametric.md) | Indicates if this feature is parametric or not. |
| [isSuppressed](DraftFeature_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isTangentChain](DraftFeature_isTangentChain.md) | Gets and sets if any faces that are tangentially connected to any of the input faces will also be drafted. It defaults to true. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isValid](DraftFeature_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](DraftFeature_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [name](DraftFeature_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [nativeObject](DraftFeature_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](DraftFeature_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentComponent](DraftFeature_parentComponent.md) | Returns the parent component that owns this feature. |
| [plane](DraftFeature_plane.md) | Gets and sets the plane that defines the direction in which the draft is applied. This is also referred to as the pull direction. This can be defined using either a planar BrepFace, or a ConstructionPlane. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [timelineObject](DraftFeature_timelineObject.md) | Returns the timeline object associated with this feature. |

## Accessed From

[DraftFeature.createForAssemblyContext](DraftFeature_createForAssemblyContext.md), [DraftFeature.nativeObject](DraftFeature_nativeObject.md), [DraftFeatures.add](DraftFeatures_add.md), [DraftFeatures.item](DraftFeatures_item.md), [DraftFeatures.itemByName](DraftFeatures_itemByName.md)

## Samples

| Name | Description |
|----|----|
| [Draft Feature API Sample](DraftFeatureSample_Sample.md) | Demonstrates creating a new draft feature. |

## Version

Introduced in version January 2015  

