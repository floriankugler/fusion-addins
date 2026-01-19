# ChamferFeature Object

Derived from: [Feature](Feature.md) Object  

## Description

Object that represents an existing chamfer feature in a design.

## Methods

| Name | Description |
|----|----|
| [classType](ChamferFeature_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](ChamferFeature_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](ChamferFeature_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](ChamferFeature_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |
| [setDistanceAndAngle](ChamferFeature_setDistanceAndAngle.md) | \*\*RETIRED\*\* Changes the type of chamfer to be a distance and angle chamfer. |
| [setEqualDistance](ChamferFeature_setEqualDistance.md) | \*\*RETIRED\*\* Changes the type of chamfer to be an equal distance chamfer. |
| [setTwoDistances](ChamferFeature_setTwoDistances.md) | \*\*RETIRED\*\* Changes the type of chamfer to be a two distances chamfer. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](ChamferFeature_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](ChamferFeature_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](ChamferFeature_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bodies](ChamferFeature_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [chamferType](ChamferFeature_chamferType.md) | **RETIRED** Gets an enum indicating how the chamfer was defined. The valid return values are EqualDistanceType, TwoDistancesType and DistanceAndAngleType. This property returns nothing in the case where the feature is non-parametric. |
| [chamferTypeDefinition](ChamferFeature_chamferTypeDefinition.md) | **RETIRED** Gets the definition object that is defining the type of chamfer. Modifying the definition object will cause the chamfer to recompute. Various types of definition objects can be returned depending on how the chamfer is defined. The ChamferType property can be used to determine which type of definition will be returned. This property returns nothing in the case where the feature is non-parametric. |
| [cornerType](ChamferFeature_cornerType.md) | Gets and sets the type of corner to be modeled when multiple edges connect at a vertex. |
| [edges](ChamferFeature_edges.md) | **RETIRED** Gets and sets the edges being chamfered. Specific edges can be defined using one or more BRepEdge objects or BRepFace objects can be used to chamfer all edges of the face or Feature objects can be used to chamfer all edges associated with the input features. If BRepEdge objects are provided and the isTangentChain argument is true additional edges may also get chamfered if they are tangentially connected to any of the input edges. When getting the property, your code should check for the different types in the returned collection and handle it appropriately. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) This property returns nothing in the case where the feature is non-parametric. |
| [edgeSets](ChamferFeature_edgeSets.md) | Returns the edge sets associated with this chamfer. |
| [entityToken](ChamferFeature_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](ChamferFeature_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [faces](ChamferFeature_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [healthState](ChamferFeature_healthState.md) | Returns the current health state of the feature. |
| [isParametric](ChamferFeature_isParametric.md) | Indicates if this feature is parametric or not. |
| [isSuppressed](ChamferFeature_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isTangentChain](ChamferFeature_isTangentChain.md) | **RETIRED** Gets and sets whether or not edges that are tangentially connected to the input edges (if any) will also be chamfered. |
| [isValid](ChamferFeature_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](ChamferFeature_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [name](ChamferFeature_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [nativeObject](ChamferFeature_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](ChamferFeature_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentComponent](ChamferFeature_parentComponent.md) | Returns the parent component that owns this feature. |
| [timelineObject](ChamferFeature_timelineObject.md) | Returns the timeline object associated with this feature. |

## Accessed From

[ChamferFeature.createForAssemblyContext](ChamferFeature_createForAssemblyContext.md), [ChamferFeature.nativeObject](ChamferFeature_nativeObject.md), [ChamferFeatures.add](ChamferFeatures_add.md), [ChamferFeatures.item](ChamferFeatures_item.md), [ChamferFeatures.itemByName](ChamferFeatures_itemByName.md), [ChamferTypeDefinition.parentFeature](ChamferTypeDefinition_parentFeature.md), [DistanceAndAngleChamferTypeDefinition.parentFeature](DistanceAndAngleChamferTypeDefinition_parentFeature.md), [EqualDistanceChamferTypeDefinition.parentFeature](EqualDistanceChamferTypeDefinition_parentFeature.md), [TwoDistancesChamferTypeDefinition.parentFeature](TwoDistancesChamferTypeDefinition_parentFeature.md)

## Version

Introduced in version November 2014  

