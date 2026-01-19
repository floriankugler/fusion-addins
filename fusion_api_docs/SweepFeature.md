# SweepFeature Object

Derived from: [Feature](Feature.md) Object  

## Description

Object that represents an existing sweep feature in a design.

## Methods

| Name | Description |
|----|----|
| [classType](SweepFeature_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](SweepFeature_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](SweepFeature_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](SweepFeature_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](SweepFeature_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](SweepFeature_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](SweepFeature_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bodies](SweepFeature_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [distanceOne](SweepFeature_distanceOne.md) | Gets the distance for the first side. This property returns nothing in the case where the feature is non-parametric. |
| [distanceTwo](SweepFeature_distanceTwo.md) | Gets the distance for the second side. Returns nothing if the path is only on one side of the profile or if the sweep definition includes a guide rail or surface. It's always the distance against the normal of the profile if available. This property returns nothing in the case where the feature is non-parametric. |
| [endFaces](SweepFeature_endFaces.md) | Property that returns the set of that cap one end of the sweep that are coincident with the sketch plane. The end faces are those not coincident to the sketch plane of the feature's profile. In the case of a symmetric revolution these faces are the ones on the negative normal side of the sketch plane. In the cases where there aren't any end faces this property will return Nothing. |
| [entityToken](SweepFeature_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](SweepFeature_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [extent](SweepFeature_extent.md) | Gets and sets the sweep extent type. It defaults to PerpendicularToPathExtentType. When sweeping a solid setting the twist angle requires the solid twist axis to be set. This property is ignored when a guide rail has not been specified. |
| [faces](SweepFeature_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [guideRail](SweepFeature_guideRail.md) | Gets and sets the guide rail to create the sweep. This can be set to null to have a path only sweep. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [guideSurfaces](SweepFeature_guideSurfaces.md) | Gets and sets the guide surfaces to create the sweep. This can be set to an empty array to remove the guide surfaces and have a single path sweep feature. The isChainSelection property controls whether tangentially connected faces to the guide surfaces are also made guide surfaces. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [healthState](SweepFeature_healthState.md) | Returns the current health state of the feature. |
| [isChainSelection](SweepFeature_isChainSelection.md) | Get and sets whether faces that are tangentially connected to the guide surfaces are also made guide surfaces. |
| [isDirectionFlipped](SweepFeature_isDirectionFlipped.md) | Gets and sets if the direction of the sweep is flipped. This property only applies to sweep features that include a guide rail and whose path runs on both sides of the profile. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isParametric](SweepFeature_isParametric.md) | Indicates if this feature is parametric or not. |
| [isSolid](SweepFeature_isSolid.md) | Indicates if this feature was initially created as a solid or a surface. |
| [isSuppressed](SweepFeature_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isValid](SweepFeature_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](SweepFeature_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [name](SweepFeature_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [nativeObject](SweepFeature_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](SweepFeature_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](SweepFeature_operation.md) | Gets and sets the type of operation performed by the sweep. |
| [orientation](SweepFeature_orientation.md) | Gets and sets the sweep orientation. It defaults to PerpendicularOrientationType. This property is ignored if sweeping a solid or a guide rail or surface has been specified. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [parentComponent](SweepFeature_parentComponent.md) | Returns the parent component that owns this feature. |
| [participantBodies](SweepFeature_participantBodies.md) | Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [path](SweepFeature_path.md) | Gets and sets the path to create the sweep. This property returns nothing in the case where the feature is non-parametric. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [profile](SweepFeature_profile.md) | Gets and sets the profiles or planar faces used to define the shape of the sweep. This property can return or be set with a single Profile, a single planar face, or an ObjectCollection consisting of multiple profiles and planar faces. When an ObjectCollection is used all of the profiles and faces must be co-planar. This property returns nothing in the case where the feature is non-parametric. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [profileScaling](SweepFeature_profileScaling.md) | Gets and sets the sweep profile scaling option. It defaults to SweepProfileScaleOption. This property is only used when a guide rail has been specified. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [sideFaces](SweepFeature_sideFaces.md) | Property that returns an object that provides access to all of the faces created around the perimeter of the feature. |
| [solidAlignedAxis](SweepFeature_solidAlignedAxis.md) | Gets and sets the axis to align the solid being swept with. The axis is used when sweeping a solid, and the solid orientation is set to AlignedSolidOrientationType. It can be a sketch line, linear edge, or construction axis. |
| [solidBody](SweepFeature_solidBody.md) | Gets and sets the BRepBody object to sweep. It must be a solid body. Setting this property results in the type being a single path sweep, and if the profile, guide path, or surface are set, they are set to null. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [solidOrientation](SweepFeature_solidOrientation.md) | Gets and sets the sweep solid orientation. It defaults to PerpendicularSolidOrientationType. Setting the solid orientation to AlignedSolidOrientationType requires the solid aligned axis to be set. This property is ignored if sweeping a profile. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [solidTwistAxis](SweepFeature_solidTwistAxis.md) | Gets and sets the twist axis of the solid being swept. The axis is used when sweeping a solid, and the twist angle is set. It can be a sketch line, linear edge, construction axis, or a face that defines an axis (cylinder, cone, torus, etc.). |
| [startFaces](SweepFeature_startFaces.md) | Property that returns the set of that cap one end of the sweep that are coincident with the sketch plane. In the cases where there aren't any start faces this property will return Nothing. |
| [taperAngle](SweepFeature_taperAngle.md) | Gets the ModelParameter that defines the taper angle of the sweep feature. The value of the angle can be edited by using the properties on the ModelParameter object to edit the parameter. This property is ignored if sweeping a solid or a guide rail or surface has been specified. |
| [timelineObject](SweepFeature_timelineObject.md) | Returns the timeline object associated with this feature. |
| [twistAngle](SweepFeature_twistAngle.md) | Gets the ModelParameter that defines the twist angle of the sweep feature. The value of the angle can be edited by using the properties on the ModelParameter object to edit the parameter. When sweeping a solid setting the twist angle requires the solid twist axis to be set. This property is ignored if a guide rail or surface has been specified. |

## Accessed From

[SweepFeature.createForAssemblyContext](SweepFeature_createForAssemblyContext.md), [SweepFeature.nativeObject](SweepFeature_nativeObject.md), [SweepFeatures.add](SweepFeatures_add.md), [SweepFeatures.item](SweepFeatures_item.md), [SweepFeatures.itemByName](SweepFeatures_itemByName.md)

## Samples

| Name | Description |
|----|----|
| [Sweep Feature API Sample](SweepFeatureSample_Sample.md) | Demonstrates creating a new sweep feature. |
| [Sweep with guide rail Feature API Sample](SweepWithGuideRailFeatureSample_Sample.md) | Demonstrates creating a new Sweep feature that uses a guide rail along with a profile. |
| [Two Rail Sweep Feature API Sample](TwoRailSweepFeatureSample_Sample.md) | Demonstrates creating new two rail sweep feature. |

## Version

Introduced in version November 2014  

