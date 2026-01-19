# BossFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a boss feature or a boss connection

## Methods

| Name | Description |
|----|----|
| [classType](BossFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createSideInput](BossFeatureInput_createSideInput.md) | Creates a new BossFeatureSideInput object that is used to specify the input for boss feature side. This object can be set to side1 or side2. Side1 is meant to be side where screw head engages with the boss and Side2 is meant to be a side where screw thread engages with the part or metal inserts. |
| [setPositionBySketchPoints](BossFeatureInput_setPositionBySketchPoints.md) | Defines the position and orientation of the boss feature using a sketch point(s). |

## Properties

| Name | Description |
| --- | --- |
| [creationOccurrence](BossFeatureInput_creationOccurrence.md) | In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the boss feature is created based on geometry (e.g. point) in another component AND (the boss) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI A value of null indicates that everything is in the context of a single component. The occurrence provided sets scope for detection of target participant bodies. |
| [isDefaultDirection](BossFeatureInput_isDefaultDirection.md) | Get or set if the boss feature (or boss connection) goes in the default direction or is reversed. |
| [isValid](BossFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BossFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offset](BossFeatureInput_offset.md) | Get or set offset of the parting face from the selected position point. |
| [participantBodies](BossFeatureInput_participantBodies.md) | Gets and sets the list of bodies that will participate in the boss feature. If body provided does not intersect with direction vector at proposed position points it will be ignored. If more bodies intersect at given position point only the closest body will be accepted. Boss feature works with solid bodies only. If this property has not been set (or is empty) closest visible bodies will be detected automatically based on proposed positions and orientation. |
| [side1](BossFeatureInput_side1.md) | Gets or sets inputs for top side of the boss feature connection. It is the side where screw head engages with the boss. Default Side1 direction is considered direction of Z-axis of the parent sketch for selected position point. |
| [side2](BossFeatureInput_side2.md) | Gets or sets inputs for bottom side of the boss feature connection. It is the side where screw thread engages with the part or metal insert. Default Side2 direction is considered opposite to the direction Z-axis of the parent sketch for selected position point. |
| [targetBaseFeature](BossFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[BossFeature.createInput](BossFeature_createInput.md), [BossFeatures.createInput](BossFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

