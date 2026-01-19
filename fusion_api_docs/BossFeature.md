# BossFeature Object

Derived from: [Feature](Feature.md) Object  

## Description

Object that represents an existing boss feature in a design. For history free model this interface has limited functionality.

## Methods

| Name | Description |
|----|----|
| [classType](BossFeature_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](BossFeature_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [createInput](BossFeature_createInput.md) | Creates object with inputs this feature represents. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |
| [deleteMe](BossFeature_deleteMe.md) | Deletes the feature. This works for both parametric and non-parametric features. |
| [dissolve](BossFeature_dissolve.md) | Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features. |
| [update](BossFeature_update.md) | Changes the boss feature (or boss connection) to the input provided. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |

## Properties

| Name | Description |
| --- | --- |
| [alignmentDepth](BossFeature_alignmentDepth.md) | Returns the model parameter controlling the step depth used for alignment of its counterparts. |
| [alignmentDiameter](BossFeature_alignmentDiameter.md) | Returns the model parameter controlling the step diameter used for alignment of its counterparts. |
| [alignmentDraftAngle](BossFeature_alignmentDraftAngle.md) | Returns the model parameter controlling the step draft angle. |
| [alignmentRootRadius](BossFeature_alignmentRootRadius.md) | Returns the model parameter controlling blend radius of the boss alignment root. |
| [alignmentTipRadius](BossFeature_alignmentTipRadius.md) | Returns the model parameter controlling blend radius of the boss alignment top face. |
| [alignmentType](BossFeature_alignmentType.md) | Returns the current boss alignment shape this feature represents. |
| [assemblyContext](BossFeature_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](BossFeature_attributes.md) | Returns the collection of attributes associated with this face. |
| [baseFeature](BossFeature_baseFeature.md) | If this feature is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [bodies](BossFeature_bodies.md) | Returns the bodies that were modified or created by this feature. This property works for both parametric and non-parametric features. For a BaseFeature, this property has two different behaviors depending on if the BaseFeature is active for edit or not. When the base feature is active, this property returns the bodies owned by the base feature or the source bodies. When the base feature is not active, this property returns the result bodies. When a body is added to a base feature, that body is owned by the base feature and is only seen in the UI when the base feature is active. This body is referred to as a "source body". Fusion creates a parametric copy of the body when you exit the base feature. This copy is referred to as the "result body," and it is used for subsequent modeling operations. You can map between the source and result bodies by using their position within the bodies returned. To get a valid list of result bodies, you should roll the timeline to immediately after the base feature node in the timeline. Otherwise, subsequent operations could have done something to cause one or more bodies to no longer be available. |
| [diameter](BossFeature_diameter.md) | Returns the model parameter controlling the shank diameter. |
| [direction](BossFeature_direction.md) | Returns the direction of the boss feature with respect to selected position point. For selected sketch point this direction represents a Z-axis of the sketch. |
| [draftAngle](BossFeature_draftAngle.md) | Returns the model parameter controlling the shank draft angle. |
| [entityToken](BossFeature_entityToken.md) | Returns a token for the Feature object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same feature. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](BossFeature_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [faces](BossFeature_faces.md) | Returns the faces that were created by this feature. This works for both parametric and non-parametric features. Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available. |
| [healthState](BossFeature_healthState.md) | Returns the current health state of the feature. |
| [holeCountersinkAngle](BossFeature_holeCountersinkAngle.md) | Returns the model parameter controlling countersink angle for countersink hole. If hole type is not set to countersink hole or boss shape is to BossBlank this parameter is unused. |
| [holeDepth](BossFeature_holeDepth.md) | Returns the model parameter controlling the hole depth with respect to hole extent type. If hole extent type is set to BossHoleThrough parameter not used. If hole extent type is BossBlindFull the parameter is a distance from farthest face. If hole extent type is set to BossBlindDepth the parameter is a distance from start face of the hole. |
| [holeDiameter](BossFeature_holeDiameter.md) | Returns the model parameter controlling the hole diameter. |
| [holeDraftAngle](BossFeature_holeDraftAngle.md) | Returns the model parameter controlling hole draft angle. |
| [holeEndRadius](BossFeature_holeEndRadius.md) | Returns the model parameter controlling blend radius of the hole end. |
| [holeExtentType](BossFeature_holeExtentType.md) | Returns the current type of hole extent this feature represents. |
| [holeMajorDepth](BossFeature_holeMajorDepth.md) | Returns the model parameter controlling major hole depth for counterbore and countersink hole. If hole type is set to simple hole or boss shape is to BossBlank this parameter is unused. |
| [holeMajorDiameter](BossFeature_holeMajorDiameter.md) | Returns the model parameter controlling major hole diameter for counterbore and countersink hole. If hole type is set to simple hole or boss shape is to BossBlank this parameter is unused. |
| [holeMajorDraftAngle](BossFeature_holeMajorDraftAngle.md) | Returns the model parameter controlling major hole draft angle for counterbore and countersink hole. If hole type is set to simple hole or boss shape is to BossBlank this parameter is unused. |
| [holeMajorRootRadius](BossFeature_holeMajorRootRadius.md) | Returns the model parameter controlling blend radius of major hole counterbore root. |
| [holeMajorTipRadius](BossFeature_holeMajorTipRadius.md) | Returns the model parameter controlling blend radius of major hole counterbore. |
| [holeStartRadius](BossFeature_holeStartRadius.md) | Returns the model parameter controlling blend radius of the hole start. |
| [holeType](BossFeature_holeType.md) | Returns the current type of hole this feature represents. |
| [innerRadius](BossFeature_innerRadius.md) | Returns the model parameter for inner radius - reference for parametric expressions. |
| [isDirectionFlipped](BossFeature_isDirectionFlipped.md) | Gets and sets if the direction of the boss (or boss connection) is flipped. |
| [isGeometryOpposite](BossFeature_isGeometryOpposite.md) | Gets if this boss feature instance represents a bottom side where screw thread engages with the part. If this feature instance represents a geometry where screw head engages it returns false. |
| [isParametric](BossFeature_isParametric.md) | Indicates if this feature is parametric or not. |
| [isSuppressed](BossFeature_isSuppressed.md) | Gets and sets if this feature is suppressed. This is only valid for parametric features. |
| [isValid](BossFeature_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linkedFeatures](BossFeature_linkedFeatures.md) | Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface. |
| [name](BossFeature_name.md) | Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric). |
| [nativeObject](BossFeature_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](BossFeature_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offset](BossFeature_offset.md) | Returns the model parameter controlling the offset from the selected parting plane. |
| [offsetClearance](BossFeature_offsetClearance.md) | Returns the model parameter controlling the offset clearance from the selected parting plane and offset. |
| [parentComponent](BossFeature_parentComponent.md) | Returns the parent component that owns this feature. |
| [positionDefinition](BossFeature_positionDefinition.md) | Returns a BossPositionDefinition object that provides access to the information used to define the position of the boss feature. |
| [ribBlendRadius](BossFeature_ribBlendRadius.md) | Returns the model parameter controlling size of rib root blend radius. |
| [ribChamferAngle](BossFeature_ribChamferAngle.md) | Returns the model parameter controlling size of rib chamfer angle. |
| [ribCount](BossFeature_ribCount.md) | Returns the model parameter controlling number of ribs. |
| [ribCutSize](BossFeature_ribCutSize.md) | Returns the model parameter controlling size of rib chamfer or fillet. |
| [ribDraftAngle](BossFeature_ribDraftAngle.md) | Returns the model parameter controlling ribs draft angle. |
| [ribLength](BossFeature_ribLength.md) | Returns the model parameter controlling ribs length measured from the shank axis. |
| [ribOffset](BossFeature_ribOffset.md) | Returns the model parameter controlling ribs offset from the top face or alignment face. |
| [ribOuterDraftAngle](BossFeature_ribOuterDraftAngle.md) | Returns the model parameter controlling size of rib outer draft angle. |
| [ribRotation](BossFeature_ribRotation.md) | Returns the model parameter controlling rotation angle of the first rib from the reference vector. For selected sketch point(s) the direction of reference vector is X-axis of the parent sketch. |
| [ribThickness](BossFeature_ribThickness.md) | Returns the model parameter controlling ribs thickness. |
| [ribTipRadius](BossFeature_ribTipRadius.md) | Returns the model parameter controlling size of rib tip blend radius. |
| [ribTotalAngle](BossFeature_ribTotalAngle.md) | Returns the model parameter controlling total angle for ribs distribution. |
| [ribType](BossFeature_ribType.md) | Returns the current type of ribs shape this feature represents. |
| [rootRadius](BossFeature_rootRadius.md) | Returns the model parameter controlling blend radius of the boss shank. |
| [screwDiameter](BossFeature_screwDiameter.md) | Returns the model parameter for screw diameter - reference for parametric expressions. |
| [screwHeadAngle](BossFeature_screwHeadAngle.md) | Returns the model parameter for countersink head angle - reference for parametric expressions. |
| [screwHeadDiameter](BossFeature_screwHeadDiameter.md) | Returns the model parameter for screw head diameter - reference for parametric expressions. |
| [shapeType](BossFeature_shapeType.md) | Returns the current boss shape this feature represents. |
| [taperAngle](BossFeature_taperAngle.md) | Returns the model parameter for taper angle - plastic part rule reference. |
| [thickness](BossFeature_thickness.md) | Returns the model parameter for thickness - plastic part rule reference. |
| [timelineObject](BossFeature_timelineObject.md) | Returns the timeline object associated with this feature. |
| [tipRadius](BossFeature_tipRadius.md) | Returns the model parameter controlling blend radius of the boss shank top face. |

## Accessed From

[BossFeature.createForAssemblyContext](BossFeature_createForAssemblyContext.md), [BossFeature.nativeObject](BossFeature_nativeObject.md), [BossFeatures.add](BossFeatures_add.md), [BossFeatures.item](BossFeatures_item.md), [BossFeatures.itemByName](BossFeatures_itemByName.md)

## Version

Introduced in version October 2022  

