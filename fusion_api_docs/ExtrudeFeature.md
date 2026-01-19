# ExtrudeFeature Object

Derived from: [Feature](Feature.md) Object  

## Description

Object that represents an existing extrude feature in a design.

## Methods

| Name | Description |
| --- | --- |
| [classType](ExtrudeFeature_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](ExtrudeFeature_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](ExtrudeFeature_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](ExtrudeFeature_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |
| [setOneSideExtent](ExtrudeFeature_setOneSideExtent.md) | Redefines the extrusion to go in one direction from the profile. The extent of the extrusion is defined by the extent argument. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [setSymmetricExtent](ExtrudeFeature_setSymmetricExtent.md) | Redefines the extrusion to go symmetrically in both directions from the profile. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [setThinExtrude](ExtrudeFeature_setThinExtrude.md) | Changes the extrude feature to be a thin extrude. This is only valid if the isThinExtrude property is False. If the extrusion is already a thin extrude, you can use the properties on the ExtrudeFeature to modify the thin extrude specific values. |
| [setTwoSidesExtent](ExtrudeFeature_setTwoSidesExtent.md) | Redefines the extrusion to go in both directions from the profile. The extent is defined independently for each direction using the input arguments. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](ExtrudeFeature_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](ExtrudeFeature_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](ExtrudeFeature_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bodies](ExtrudeFeature_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [endFaces](ExtrudeFeature_endFaces.md) | Property that returns the set of faces that cap the end of the extrusion, opposite the start faces. In the case where there are no end faces, this property will return null. |
| [entityToken](ExtrudeFeature_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](ExtrudeFeature_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [extentOne](ExtrudeFeature_extentOne.md) | Gets and sets the extent used for a single sided extrude or side one of a two-sided extrusion. Valid inputs are DistanceExtentDefinition, ToEntityExtentDefinition, and ThroughAllExtentDefinition object, which can be created statically using the create method on the classes. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [extentTwo](ExtrudeFeature_extentTwo.md) | Gets and sets the extent used for side two of the extrusion. If the extrude is a single sided extrude this property will return null and will fail if set. The hasTwoExtents property can be used to determine if there are two sides or not. When setting this property, valid inputs are DistanceExtentDefinition, ToEntityExtentDefinition, and ThroughAllExtentDefinition object, which can be created statically using the create method on the classes. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [extentType](ExtrudeFeature_extentType.md) | Returns a value indicating how the extent is defined for this extrude. |
| [faces](ExtrudeFeature_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [hasTwoExtents](ExtrudeFeature_hasTwoExtents.md) | Property that indicates if the extrusion is a single or two-sided extrusion. If false, the extentTwo and taperAngleTwo properties should not be used. |
| [healthState](ExtrudeFeature_healthState.md) | Returns the current health state of the feature. |
| [isParametric](ExtrudeFeature_isParametric.md) | Indicates if this feature is parametric or not. |
| [isSolid](ExtrudeFeature_isSolid.md) | Indicates if this feature was initially created as a solid or a surface. |
| [isSuppressed](ExtrudeFeature_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isThinExtrude](ExtrudeFeature_isThinExtrude.md) | Sets or returns whether the extrude is a thin extrude. Setting it as false will make it a regular extrude. |
| [isValid](ExtrudeFeature_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](ExtrudeFeature_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [name](ExtrudeFeature_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [nativeObject](ExtrudeFeature_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](ExtrudeFeature_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](ExtrudeFeature_operation.md) | Gets and sets the type of operation performed by the extrusion. |
| [parentComponent](ExtrudeFeature_parentComponent.md) | Returns the parent component that owns this feature. |
| [participantBodies](ExtrudeFeature_participantBodies.md) | Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [profile](ExtrudeFeature_profile.md) | Gets and sets the profiles or planar faces used to define the shape of the extrude. This property can return or be set with a single Profile, a single planar face, or an ObjectCollection consisting of multiple profiles and planar faces. When an ObjectCollection is used all of the profiles and faces must be co-planar. When setting this property of a surface (non-solid) extrusion, you can use the createOpenProfile and createBRepEdgeProfile methods of the Component object to create an open profile. This property returns null in the case where the feature is non-parametric. |
| [sideFaces](ExtrudeFeature_sideFaces.md) | Property that returns all of the side faces (i.e. those running perpendicular to the extrude direction) of the feature. |
| [startExtent](ExtrudeFeature_startExtent.md) | Gets and sets the extent used to define the start of the extrusion. You can set this property with either a ProfilePlaneStartDefinition, OffsetStartDefinition or a EntityStartDefinition object. You can get any of those objects by using the static create method on the class. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [startFaces](ExtrudeFeature_startFaces.md) | Property that returns the set of faces that cap the end of the extrusion and are coincident with the sketch plane. In the case of a symmetric extrusion, these faces are the ones on the positive normal side of the sketch plane. In the case where there are no start faces, this property will return null. |
| [symmetricExtent](ExtrudeFeature_symmetricExtent.md) | If the current extent of the feature is defined as a symmetric extent, this property returns the SymmericExtentDefinition object that provides access to the information defining the symmetric extent. If the current extent is not symmetric, this property returns null. You can determine the type of extent by using the extentType property. To change the extent of a feature to symmetric extent you can use the setSymmetricExtent method. |
| [taperAngleOne](ExtrudeFeature_taperAngleOne.md) | Gets the parameter controlling the taper angle for a single sided extrusion or side one of a two-sided extrusion. To edit the angle, use properties on the parameter to change the value of the parameter. |
| [taperAngleTwo](ExtrudeFeature_taperAngleTwo.md) | Gets the parameter controlling the taper angle for side two of a two-sided extrusion. if the extrusion is single-sided, this property will return null. The hasTwoExtents property can be used to determine if there are two sides or not. To edit the angle, use properties on the parameter to change the value of the parameter. |
| [thinExtrudeWallLocationOne](ExtrudeFeature_thinExtrudeWallLocationOne.md) | Gets and sets the wall location for a one sided thin extrude or side one of a two sided thin extrude |
| [thinExtrudeWallLocationTwo](ExtrudeFeature_thinExtrudeWallLocationTwo.md) | Gets and sets the wall location for side two of a two sided thin extrude |
| [thinExtrudeWallThicknessOne](ExtrudeFeature_thinExtrudeWallThicknessOne.md) | Gets and sets the wall thickness for a one sided thin extrude or side one of a two sided thin extrude |
| [thinExtrudeWallThicknessTwo](ExtrudeFeature_thinExtrudeWallThicknessTwo.md) | Gets and sets the wall thickness for side two of a two sided thin extrude |
| [timelineObject](ExtrudeFeature_timelineObject.md) | Returns the timeline object associated with this feature. |

## Accessed From

[ExtrudeFeature.createForAssemblyContext](ExtrudeFeature_createForAssemblyContext.md), [ExtrudeFeature.nativeObject](ExtrudeFeature_nativeObject.md), [ExtrudeFeatures.add](ExtrudeFeatures_add.md), [ExtrudeFeatures.addSimple](ExtrudeFeatures_addSimple.md), [ExtrudeFeatures.item](ExtrudeFeatures_item.md), [ExtrudeFeatures.itemByName](ExtrudeFeatures_itemByName.md)

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |
| [Move Feature API Sample](MoveFeatureSample_Sample.md) | Demonstrates creating a new move feature. |
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |
| [ReplaceFace Feature](ReplaceFaceFeatureSample_Sample.md) | Demonstrates creating a new replaceface feature. |
| [Shell Feature API Sample](ShellFeatureSample_Sample.md) | Demonstrates creating a new shell feature. |

## Version

Introduced in version August 2014  

