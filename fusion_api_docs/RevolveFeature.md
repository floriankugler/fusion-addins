# RevolveFeature Object

Derived from: [Feature](Feature.md) Object  

## Description

Object that represents an existing revolve feature in a design.

## Methods

| Name | Description |
| --- | --- |
| [classType](RevolveFeature_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](RevolveFeature_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](RevolveFeature_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](RevolveFeature_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |
| [setAngleExtent](RevolveFeature_setAngleExtent.md) | Defines the extent of the revolution to be at a defined angle. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [setOneSideToExtent](RevolveFeature_setOneSideToExtent.md) | Changes the extent of the revolve to be from the sketch plane to the specified "to" face. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [setTwoSideAngleExtent](RevolveFeature_setTwoSideAngleExtent.md) | Changes the extent of the revolve to be defined as a two sided angle extent. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [setTwoSidesToExtent](RevolveFeature_setTwoSidesToExtent.md) | Changes the extent of the revolve to be defined as a two sided to extent. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](RevolveFeature_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](RevolveFeature_attributes.md) | Returns the collection of attributes associated with this face. |
| [axis](RevolveFeature_axis.md) | Gets and sets the entity used to define the axis of revolution. The axis can be a sketch line, construction axis, linear edge or a face that defines an axis (cylinder, cone, torus, etc.). If it is not in the same plane as the profile, it is projected onto the profile plane. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [baseFeature](RevolveFeature_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bodies](RevolveFeature_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [endFaces](RevolveFeature_endFaces.md) | Property that returns the set of faces that cap the end of the revolve opposite the start faces. In the case where there aren't any start faces, this property will return null. |
| [entityToken](RevolveFeature_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](RevolveFeature_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [extentDefinition](RevolveFeature_extentDefinition.md) | Gets the definition object that is defining the extent of the revolve. Modifying the definition object will cause the revolve to recompute. Various types of objects can be returned depending on the type of extent currently defined for the revolve. This property returns nothing in the case where the feature is non-parametric. |
| [faces](RevolveFeature_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [healthState](RevolveFeature_healthState.md) | Returns the current health state of the feature. |
| [isParametric](RevolveFeature_isParametric.md) | Indicates if this feature is parametric or not. |
| [isProjectAxis](RevolveFeature_isProjectAxis.md) | Specifies if the axis should be projected on the same plane as the profile sketch plane or not. Setting this to true will use a projected axis, while setting it to false will keep it in its original location. This is initialized to false so the selected axis will be used in the feature. |
| [isSolid](RevolveFeature_isSolid.md) | Indicates if this feature was initially created as a solid or a surface. |
| [isSuppressed](RevolveFeature_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isValid](RevolveFeature_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](RevolveFeature_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [name](RevolveFeature_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [nativeObject](RevolveFeature_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](RevolveFeature_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](RevolveFeature_operation.md) | Gets and sets the type of operation performed by the revolve. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [parentComponent](RevolveFeature_parentComponent.md) | Returns the parent component that owns this feature. |
| [participantBodies](RevolveFeature_participantBodies.md) | Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [profile](RevolveFeature_profile.md) | Gets and sets the profiles or planar faces used to define the shape of the revolve. This property can return or be set with a single Profile, a single planar face, or an ObjectCollection consisting of multiple profiles and planar faces. When an ObjectCollection is used all of the profiles and faces must be co-planar. When setting this property of a surface (non-solid) extrusion, you can use the createOpenProfile and createBRepEdgeProfile methods of the Component object to create an open profile. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) This property returns null in the case where the feature is non-parametric. |
| [sideFaces](RevolveFeature_sideFaces.md) | Property that returns all of the faces created around the perimeter of the feature. |
| [startFaces](RevolveFeature_startFaces.md) | Property that returns the set of faces that cap one end of the revolve and are coincident with the sketch plane. In the case of a symmetric revolve these faces are the ones on the positive normal side of the sketch plane. In the case where there aren't any start faces, this property will return null. |
| [timelineObject](RevolveFeature_timelineObject.md) | Returns the timeline object associated with this feature. |

## Accessed From

[RevolveFeature.createForAssemblyContext](RevolveFeature_createForAssemblyContext.md), [RevolveFeature.nativeObject](RevolveFeature_nativeObject.md), [RevolveFeatures.add](RevolveFeatures_add.md), [RevolveFeatures.item](RevolveFeatures_item.md), [RevolveFeatures.itemByName](RevolveFeatures_itemByName.md)

## Version

Introduced in version August 2014  

