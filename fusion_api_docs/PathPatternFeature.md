# PathPatternFeature Object

Derived from: [Feature](Feature.md) Object  

## Description

Object that represents an existing path pattern feature in a design.

## Methods

| Name | Description |
|----|----|
| [classType](PathPatternFeature_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](PathPatternFeature_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](PathPatternFeature_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](PathPatternFeature_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](PathPatternFeature_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](PathPatternFeature_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](PathPatternFeature_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bodies](PathPatternFeature_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [distance](PathPatternFeature_distance.md) | Gets the distance. Edit the value through ModelParameter. Returns nothing in the case where the feature is non-parametric. |
| [entityToken](PathPatternFeature_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](PathPatternFeature_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [faces](PathPatternFeature_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [healthState](PathPatternFeature_healthState.md) | Returns the current health state of the feature. |
| [inputEntities](PathPatternFeature_inputEntities.md) | Gets and sets the input entities. The collection can contain faces, features, bodies or occurrences. All of the entities must be of a single type. For example, it can't contain features and occurrences but only features or occurrences. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isFlipDirection](PathPatternFeature_isFlipDirection.md) | Gets and sets if flip the direction from start point. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isOrientationAlongPath](PathPatternFeature_isOrientationAlongPath.md) | Gets and sets if the orientation is along path. If false, the orientation is identical. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isParametric](PathPatternFeature_isParametric.md) | Indicates if this feature is parametric or not. |
| [isSuppressed](PathPatternFeature_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isSymmetric](PathPatternFeature_isSymmetric.md) | Gets and sets if the pattern is in one direction or symmetric. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isValid](PathPatternFeature_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](PathPatternFeature_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [name](PathPatternFeature_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [nativeObject](PathPatternFeature_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](PathPatternFeature_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentComponent](PathPatternFeature_parentComponent.md) | Returns the parent component that owns this feature. |
| [path](PathPatternFeature_path.md) | Gets and sets the path to create the pattern on path. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [patternComputeOption](PathPatternFeature_patternComputeOption.md) | Gets and sets the compute option for this pattern feature. This property only applies when patterning features and is ignored in the direct modeling environment. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [patternDistanceType](PathPatternFeature_patternDistanceType.md) | Gets and sets how the distance between elements is computed. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [patternElements](PathPatternFeature_patternElements.md) | Gets the PatternElements collection that contains the elements created by this pattern. |
| [patternEntityType](PathPatternFeature_patternEntityType.md) | Returns the type of entities the pattern consists of. This can be used to help determine the type of results that will be found in the pattern elements. |
| [quantity](PathPatternFeature_quantity.md) | Gets the quantity of the elements. Edit the value through ModelParameter. Returns nothing in the case where the feature is non-parametric. |
| [resultFeatures](PathPatternFeature_resultFeatures.md) | Get the features that were created for this mirror. Returns null in the case where the feature is parametric. |
| [startPoint](PathPatternFeature_startPoint.md) | Gets and sets the start point on the path to count the distance. It's between 0 and 1. 0 means start point of the path, 1 means end point of the path. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [suppressedElementsIds](PathPatternFeature_suppressedElementsIds.md) | Gets and sets the id's of the elements to suppress. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [timelineObject](PathPatternFeature_timelineObject.md) | Returns the timeline object associated with this feature. |

## Accessed From

[PathPatternFeature.createForAssemblyContext](PathPatternFeature_createForAssemblyContext.md), [PathPatternFeature.nativeObject](PathPatternFeature_nativeObject.md), [PathPatternFeatures.add](PathPatternFeatures_add.md), [PathPatternFeatures.item](PathPatternFeatures_item.md), [PathPatternFeatures.itemByName](PathPatternFeatures_itemByName.md)

## Samples

| Name | Description |
|----|----|
| [Path Pattern Feature API Sample](PathPatternFeatureSample_Sample.md) | Demonstrates creating a new path pattern feature. |

## Version

Introduced in version November 2014  

