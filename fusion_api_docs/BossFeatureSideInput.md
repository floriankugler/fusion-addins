# BossFeatureSideInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a single side of boss feature

## Methods

| Name | Description |
|----|----|
| [classType](BossFeatureSideInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clearRibExtent](BossFeatureSideInput_clearRibExtent.md) | Clears rib extent types for all position points. |
| [setBlank](BossFeatureSideInput_setBlank.md) | Set boss shape into blank constant diameter shank with no hole. |
| [setCounterbore](BossFeatureSideInput_setCounterbore.md) | Set boss shape into constant diameter shank with counterbore hole. |
| [setCountersink](BossFeatureSideInput_setCountersink.md) | Set boss shape into constant diameter shank with countersink hole. |
| [setRibExtent](BossFeatureSideInput_setRibExtent.md) | Set rib extent type for particular rib for position point provided. |
| [setSimple](BossFeatureSideInput_setSimple.md) | Set boss shape into constant diameter shank with simple hole. |

## Properties

| Name | Description |
| --- | --- |
| [alignmentDepth](BossFeatureSideInput_alignmentDepth.md) | Get or set alignment depth. |
| [alignmentDiameter](BossFeatureSideInput_alignmentDiameter.md) | Get or set alignment diameter. |
| [alignmentDraftAngle](BossFeatureSideInput_alignmentDraftAngle.md) | Get or set alignment draft angle. |
| [alignmentRootRadius](BossFeatureSideInput_alignmentRootRadius.md) | Get or set blend radius of the boss alignment root. |
| [alignmentTipRadius](BossFeatureSideInput_alignmentTipRadius.md) | Get or set blend radius of the boss alignment tip. |
| [alignmentType](BossFeatureSideInput_alignmentType.md) | Get or set boss alignment shape. This usually corresponds to the alignment shape of the boss counterpart. |
| [diameter](BossFeatureSideInput_diameter.md) | Get or set boss shank diameter. |
| [draftAngle](BossFeatureSideInput_draftAngle.md) | Get or set shank draft angle. |
| [holeCountersinkAngle](BossFeatureSideInput_holeCountersinkAngle.md) | Get or set countersink angle for countersink hole. This input is used only for countersink hole. |
| [holeDepth](BossFeatureSideInput_holeDepth.md) | Get or set hole depth with respect to hole extent type. If hole extent type is set to BossHoleThrough parameter is ignored. If hole extent type is BossBlindFull the parameter is a distance from farthest face. If hole extent type is set to BossBlindDepth the parameter is a distance from start face of the hole. |
| [holeDiameter](BossFeatureSideInput_holeDiameter.md) | Get or set hole diameter. |
| [holeDraftAngle](BossFeatureSideInput_holeDraftAngle.md) | Get or set hole draft angle. |
| [holeEndRadius](BossFeatureSideInput_holeEndRadius.md) | Get or set blend radius of the hole end. |
| [holeExtentType](BossFeatureSideInput_holeExtentType.md) | Get or set hole extent this feature represents. For top side only through hole extent is accepted. |
| [holeMajorDepth](BossFeatureSideInput_holeMajorDepth.md) | Get or set major hole depth for counterbore and countersink hole or material thickness under screw head based on hole orientation in a boss feature. This input is ignored for blank boss or boss with simple hole. |
| [holeMajorDiameter](BossFeatureSideInput_holeMajorDiameter.md) | Get or set major hole diameter for counterbore or countersink hole. This input is ignored for blank boss or boss with simple hole. |
| [holeMajorDraftAngle](BossFeatureSideInput_holeMajorDraftAngle.md) | Get or set major hole draft angle for counterbore and countersink hole. This input is ignored for blank boss or boss with simple hole. |
| [holeMajorRootRadius](BossFeatureSideInput_holeMajorRootRadius.md) | Get or set blend radius of major hole counterbore root. |
| [holeMajorTipRadius](BossFeatureSideInput_holeMajorTipRadius.md) | Get or set blend radius of major hole counterbore. |
| [holeStartRadius](BossFeatureSideInput_holeStartRadius.md) | Get or set blend radius of the hole start. |
| [isValid](BossFeatureSideInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BossFeatureSideInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offsetClearance](BossFeatureSideInput_offsetClearance.md) | Get or set offset clearance as additional small offset from the selected parting plane and position point. |
| [ribChamferAngle](BossFeatureSideInput_ribChamferAngle.md) | Get or set rib chamfer angle. This input is used only for rib with chamfer. |
| [ribCount](BossFeatureSideInput_ribCount.md) | Get or set number of ribs. |
| [ribCutSize](BossFeatureSideInput_ribCutSize.md) | Get or set size of rib chamfer or fillet. |
| [ribDraftAngle](BossFeatureSideInput_ribDraftAngle.md) | Get or set ribs draft angle. |
| [ribLength](BossFeatureSideInput_ribLength.md) | Get or set ribs length measured from the shank axis. |
| [ribOffset](BossFeatureSideInput_ribOffset.md) | Get or set ribs offset from the top face or alignment face. |
| [ribOuterDraftAngle](BossFeatureSideInput_ribOuterDraftAngle.md) | Get or set rib outer draft angle. |
| [ribRootRadius](BossFeatureSideInput_ribRootRadius.md) | Get or set rib base root blend radius. |
| [ribRotation](BossFeatureSideInput_ribRotation.md) | Get or set rotation angle of the first rib from the reference vector. Reference vector is X-axis of the parent sketch from selected sketch point(s). |
| [ribThickness](BossFeatureSideInput_ribThickness.md) | Get or set ribs thickness. |
| [ribTipRadius](BossFeatureSideInput_ribTipRadius.md) | Get or set rib outer tip blend radius. |
| [ribTotalAngle](BossFeatureSideInput_ribTotalAngle.md) | Get or set total angle for ribs distribution. Default is 360 deg. |
| [ribType](BossFeatureSideInput_ribType.md) | Type of boss ribs this feature represents. |
| [rootRadius](BossFeatureSideInput_rootRadius.md) | Get or set blend radius of the boss shank and participant body. |
| [tipRadius](BossFeatureSideInput_tipRadius.md) | Get or set blend radius of the boss shank top parting face. |

## Accessed From

[BossFeatureInput.createSideInput](BossFeatureInput_createSideInput.md), [BossFeatureInput.side1](BossFeatureInput_side1.md), [BossFeatureInput.side2](BossFeatureInput_side2.md)

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

