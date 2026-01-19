# RevolveFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a revolve feature.

## Methods

| Name | Description |
|----|----|
| [classType](RevolveFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setAngleExtent](RevolveFeatureInput_setAngleExtent.md) | Defines the extent of the revolution to be at a specified angle. An angle and whether the extent is symmetric or only in one direction is specified. If it's not symmetric a positive or negative angle can be used to control the direction. If symmetric, the angle is the angle on one side so the entire angle of the revolution will be twice the specified angle. Use an angle of 360 deg or 2 pi radians to create a full revolve. |
| [setOneSideToExtent](RevolveFeatureInput_setOneSideToExtent.md) | Defines the extent of the revolve to be from the sketch or profile plane to the specified "To" face. |
| [setTwoSideAngleExtent](RevolveFeatureInput_setTwoSideAngleExtent.md) | Defines the angle of the revolve to be to applied to both sides of the profile at the specified angles. |
| [setTwoSideToExtent](RevolveFeatureInput_setTwoSideToExtent.md) | Defines the extents of the revolve to be from the sketch plane to specified faces in both directions. If the matchShape argument is true, the faces to revolve to are extended to fully intersect the revolve. |

## Properties

| Name | Description |
| --- | --- |
| [axis](RevolveFeatureInput_axis.md) | Gets and sets the entity used to define the axis of revolution. The axis can be a sketch line, construction axis, linear edge or a face that defines an axis (cylinder, cone, torus, etc.). If it is not in the same plane as the profile, it is projected onto the profile plane. |
| [creationOccurrence](RevolveFeatureInput_creationOccurrence.md) | In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Revolve is created based on geometry (e.g. a profile and/or face(s)) in another component AND (the Revolve) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI |
| [isProjectAxis](RevolveFeatureInput_isProjectAxis.md) | Specifies if the axis should be projected on the same plane as the profile sketch plane or not. Setting this to true will use a projected axis, while setting it to false will keep it in its original location. This is initialized to false so the selected axis will be used in the feature. |
| [isSolid](RevolveFeatureInput_isSolid.md) | Specifies if the revolution should be created as a solid or surface. If it's a surface then there aren't any end caps and it's open. This is initialized to true so a solid will be created if it's not changed. |
| [isValid](RevolveFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RevolveFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](RevolveFeatureInput_operation.md) | Gets and sets the type of operation performed by the revolve. |
| [participantBodies](RevolveFeatureInput_participantBodies.md) | Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection. If this property has not been set, the default behavior is that all bodies that are intersected by the feature will participate. This property can return null in the case where the feature has not been fully defined so that possible intersecting bodies can be computed. |
| [profile](RevolveFeatureInput_profile.md) | Gets and sets the profiles or planar faces used to define the shape of the revolve. This property can return or be set with a single Profile, a single planar face, or an ObjectCollection consisting of multiple profiles and planar faces. When an ObjectCollection is used all of the profiles and faces must be co-planar. This property returns null in the case where the feature is non-parametric. To create a surface (non-solid) revolution, you can use the createOpenProfile and createBRepEdgeProfile methods of the Component object to create an open profile. The isSolid property of the RevolveFeatureInput property must also be False. |
| [targetBaseFeature](RevolveFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[RevolveFeatures.createInput](RevolveFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |

## Version

Introduced in version August 2014  

