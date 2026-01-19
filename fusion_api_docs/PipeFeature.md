# PipeFeature Object

Derived from: [Feature](Feature.md) Object  

## Description

Object that represents an existing pipe feature in a design.

## Methods

| Name | Description |
| --- | --- |
| [classType](PipeFeature_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](PipeFeature_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](PipeFeature_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](PipeFeature_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |
| [setThickness](PipeFeature_setThickness.md) | Defines the section thickness of the Pipe. In case the pipe is not already hollow, this also sets the isHollow to true. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](PipeFeature_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](PipeFeature_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](PipeFeature_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bodies](PipeFeature_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [distanceOne](PipeFeature_distanceOne.md) | Gets the distance for the pipe created while following the path given as input, in the same order. If the path is open, this value returns the length of Pipe relative to the length of the path. If the path is closed, this value returns the length of the Pipe from the start point going along the curves. Ex: Path is made of curves A-B-C-A. The distanceOne returns the length of the pipe going from A-B-C-A. This property returns null in the case where the feature is non-parametric. |
| [distanceTwo](PipeFeature_distanceTwo.md) | Gets the distance for the pipe created while following the reversed path given as input. If the path is open, getting this value returns null, and setting the value is ignored. If the path is closed, this value returns the length of the Pipe from the start point going in the reverse order of the path. Ex: Path is made of curves A-B-C-A. The distanceTwo returns the length of the pipe going from A-C-B-A. This property returns null in the case where the feature is non-parametric. |
| [endFaces](PipeFeature_endFaces.md) | Property that returns the set of faces that cap one end of the Pipe that are coincident with the sketch plane. The end faces are those not coincident to the sketch plane of the feature's profile. In the case of a symmetric Pipe these faces are the ones on the negative normal side of the sketch plane. In the cases where there aren't any end faces this property will return null. |
| [entityToken](PipeFeature_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](PipeFeature_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [faces](PipeFeature_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [healthState](PipeFeature_healthState.md) | Returns the current health state of the feature. |
| [isHollow](PipeFeature_isHollow.md) | Specifies if the Pipe is hollow or not. Setting this to true will default the sectionThickness to 0.1 cm. |
| [isParametric](PipeFeature_isParametric.md) | Indicates if this feature is parametric or not. |
| [isSuppressed](PipeFeature_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isValid](PipeFeature_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](PipeFeature_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [name](PipeFeature_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [nativeObject](PipeFeature_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](PipeFeature_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](PipeFeature_operation.md) | Gets and sets the type of operation performed by the Pipe. |
| [parentComponent](PipeFeature_parentComponent.md) | Returns the parent component that owns this feature. |
| [participantBodies](PipeFeature_participantBodies.md) | Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [path](PipeFeature_path.md) | Gets and sets the path to create the Pipe. This property returns null in the case where the feature is non-parametric. The path can be either closed (you can reach again the starting point by following the curves) or open (the starting point and end point are different in the path). The starting point of the Pipe will be the starting point of the first curve in the Path, regardless of it being open or closed. When the desired Pipe has a section that includes the starting point and the path is closed, the curves should be shifted in a circular pattern. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [sectionSize](PipeFeature_sectionSize.md) | Gets and sets the section size of the Pipe. |
| [sectionThickness](PipeFeature_sectionThickness.md) | Gets the section thickness of the Pipe. If the pipe is not hollow, this will return null. |
| [sectionType](PipeFeature_sectionType.md) | Gets and sets the section type of the Pipe. The type can be: Circular, Square, Triangular. |
| [sideFaces](PipeFeature_sideFaces.md) | Property that returns an object that provides access to all of the faces created around the perimeter of the feature. |
| [startFaces](PipeFeature_startFaces.md) | Property that returns the set of faces that cap one end of the Pipe that are coincident with the sketch plane. In the cases where there aren't any start faces this property will return null. |
| [timelineObject](PipeFeature_timelineObject.md) | Returns the timeline object associated with this feature. |

## Accessed From

[PipeFeature.createForAssemblyContext](PipeFeature_createForAssemblyContext.md), [PipeFeature.nativeObject](PipeFeature_nativeObject.md), [PipeFeatures.add](PipeFeatures_add.md), [PipeFeatures.item](PipeFeatures_item.md), [PipeFeatures.itemByName](PipeFeatures_itemByName.md)

## Version

Introduced in version September 2015  

