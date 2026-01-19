# FlatPattern Object

Derived from: [Feature](Feature.md) Object  

## Description

The FlatPattern object provides access to the flattened representation of a folded part. This supports most of the functionality of a regular component like creating sketches, construction geometry, and most features. Functionality that is not supported in a flat pattern will fail if you attempt to use it. For example, the creation of occurrences and new components is not supported. Also the creation of sheet metal features is not supported.

## Methods

| Name | Description |
|----|----|
| [classType](FlatPattern_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](FlatPattern_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](FlatPattern_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |
| [getBendInfo](FlatPattern_getBendInfo.md) | Returns bend information for the specified bend. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](FlatPattern_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](FlatPattern_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](FlatPattern_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bendLinesBody](FlatPattern_bendLinesBody.md) | Returns the wire B-Rep body that represents the bend lines of the flattened sheet metal part. |
| [bodies](FlatPattern_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [bottomFace](FlatPattern_bottomFace.md) | Returns the "bottom" face of the flat pattern B-Rep body. |
| [entityToken](FlatPattern_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](FlatPattern_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [extentLinesBody](FlatPattern_extentLinesBody.md) | Returns the wire B-Rep body that represents the extent lines of the flattened sheet metal part. |
| [faces](FlatPattern_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [flatBody](FlatPattern_flatBody.md) | Returns the B-Rep body that represents the flattened sheet metal part. |
| [foldedBody](FlatPattern_foldedBody.md) | Returns the folded B-Rep body in the design that this flat pattern was created from. |
| [healthState](FlatPattern_healthState.md) | Returns the current health state of the feature. |
| [isParametric](FlatPattern_isParametric.md) | Indicates if this feature is parametric or not. |
| [isSuppressed](FlatPattern_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isValid](FlatPattern_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](FlatPattern_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [name](FlatPattern_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [objectType](FlatPattern_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentComponent](FlatPattern_parentComponent.md) | Returns the parent component that owns this feature. |
| [sideFaces](FlatPattern_sideFaces.md) | Returns the "side" faces of the flat pattern B-Rep body. These are the faces around the edge of the flat pattern that connect the top and bottom faces. |
| [timelineObject](FlatPattern_timelineObject.md) | Returns the timeline object associated with this feature. |
| [topFace](FlatPattern_topFace.md) | Returns the "top" face of the flat pattern B-Rep body. |

## Accessed From

[Component.createFlatPattern](Component_createFlatPattern.md), [Component.flatPattern](Component_flatPattern.md), [FlatPatternComponent.createFlatPattern](FlatPatternComponent_createFlatPattern.md), [FlatPatternComponent.flatPattern](FlatPatternComponent_flatPattern.md), [FlatPatternProduct.flatPattern](FlatPatternProduct_flatPattern.md)

## Version

Introduced in version October 2022  

