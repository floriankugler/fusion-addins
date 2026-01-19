# LoftFeature Object

Derived from: [Feature](Feature.md) Object  

## Description

Object that represents an existing loft feature in a design.

## Methods

| Name | Description |
|----|----|
| [classType](LoftFeature_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](LoftFeature_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](LoftFeature_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](LoftFeature_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](LoftFeature_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](LoftFeature_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](LoftFeature_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bodies](LoftFeature_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [centerLineOrRails](LoftFeature_centerLineOrRails.md) | Returns the single centerline or the set of rails that define the shape of the loft. This property returns null in the case where the feature is non-parametric. |
| [endFace](LoftFeature_endFace.md) | Property that returns the face that caps the end of the loft and is coincident with the last section. In the case where the loft isn't capped and there isn't an end face, this property will return null. |
| [endLoftEdgeAlignment](LoftFeature_endLoftEdgeAlignment.md) | Specifies the end edge alignment option for the loft feature. The default is Free Edges. |
| [entityToken](LoftFeature_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](LoftFeature_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [faces](LoftFeature_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [healthState](LoftFeature_healthState.md) | Returns the current health state of the feature. |
| [isClosed](LoftFeature_isClosed.md) | Specifies if the loft closes back on itself. In other words, the first section is also used as the last section. |
| [isParametric](LoftFeature_isParametric.md) | Indicates if this feature is parametric or not. |
| [isSolid](LoftFeature_isSolid.md) | Indicates if this feature was initially created as a solid or a surface. |
| [isSuppressed](LoftFeature_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isTangentEdgesMerged](LoftFeature_isTangentEdgesMerged.md) | Specifies if the loft will keep or merge tangent edges. These are edges between tangent faces in the resulting loft surface. If true, the faces will be merged so the connecting edge no longer exists |
| [isValid](LoftFeature_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](LoftFeature_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [loftSections](LoftFeature_loftSections.md) | Returns the set of sections that the loft passes through. This property returns null in the case where the feature is non-parametric. |
| [name](LoftFeature_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [nativeObject](LoftFeature_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](LoftFeature_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](LoftFeature_operation.md) | Gets and sets the type of operation performed by the extrusion. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [parentComponent](LoftFeature_parentComponent.md) | Returns the parent component that owns this feature. |
| [participantBodies](LoftFeature_participantBodies.md) | Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [sideFaces](LoftFeature_sideFaces.md) | Property that returns all of the side faces (i.e. those running through the sections) of the feature. |
| [startFace](LoftFeature_startFace.md) | Property that returns the face that caps the start of the loft and is coincident with the first section. In the case where the loft isn't capped and there isn't a start face, this property will return null. |
| [startLoftEdgeAlignment](LoftFeature_startLoftEdgeAlignment.md) | Specifies the start edge alignment option for the loft feature. The default is Free Edges. |
| [timelineObject](LoftFeature_timelineObject.md) | Returns the timeline object associated with this feature. |

## Accessed From

[LoftFeature.createForAssemblyContext](LoftFeature_createForAssemblyContext.md), [LoftFeature.nativeObject](LoftFeature_nativeObject.md), [LoftFeatures.add](LoftFeatures_add.md), [LoftFeatures.item](LoftFeatures_item.md), [LoftFeatures.itemByName](LoftFeatures_itemByName.md)

## Samples

| Name | Description |
|----|----|
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version September 2015  

