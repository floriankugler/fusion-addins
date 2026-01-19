# RuledSurfaceFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a Ruled Surface feature.

## Methods

| Name | Description |
|----|----|
| [classType](RuledSurfaceFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [alternateFace](RuledSurfaceFeatureInput_alternateFace.md) | Gets and sets if the other face is used for creation of the Ruled Surface. When creating a ruled surface using the edges of a solid or the interior edges of a surface the angle of the ruled surface is measured with respect to the face the selected edge is bounding. For a solid, or an interior edge on a surface, the edge connects to two faces. This setting toggles which of the two faces will be used for measuring the angle. |
| [angle](RuledSurfaceFeatureInput_angle.md) | Gets and sets the ValueInput object that defines the Ruled Surface angle. If the input is a real value, the units are radians. |
| [cornerType](RuledSurfaceFeatureInput_cornerType.md) | Gets and sets the corner type for the ruled surface, indicating if the corners will be rounded or mitered. The default value is rounded. |
| [creationOccurrence](RuledSurfaceFeatureInput_creationOccurrence.md) | In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Ruled Surface is created based on geometry (e.g. a profile) in another component AND (the Ruled Surface) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI |
| [direction](RuledSurfaceFeatureInput_direction.md) | Gets and sets the entity that defines the direction when the ruled surface type is DirectionRuledSurfaceType. The direction is specified by providing a linear or planar entity. For example, a linear edge, construction axis, planar face, or construction plane can be used as input. If this property is set when the ruledSurfaceType is not DirectionRuledSurfaceType, the type will automatically be changed to DirectionRuledSurfaceType. If you get this property when the direction is not DirectionRuledSurfaceType, it will return null. |
| [distance](RuledSurfaceFeatureInput_distance.md) | Gets and sets the ValueInput object that defines the Ruled Surface distance. If the value input is a real value it will define the distance in centimeters. |
| [isValid](RuledSurfaceFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RuledSurfaceFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](RuledSurfaceFeatureInput_operation.md) | Gets and sets the type of operation performed by the ruled surface. |
| [profile](RuledSurfaceFeatureInput_profile.md) | Gets and sets the Profile object that defines the sketch geometry or edges that define the shape of the ruled surface. The Component.createBRepEdgeProfile method is useful to create a profile defined from edges. |
| [ruledSurfaceType](RuledSurfaceFeatureInput_ruledSurfaceType.md) | Gets and sets the type of ruled surface to create. To set this to DirectionRuledSurfaceType, use the direction property to set the direction entity, which will automatically set this to DirectionRuledSurfaceType. |
| [targetBaseFeature](RuledSurfaceFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[RuledSurfaceFeatures.createInput](RuledSurfaceFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Ruled Surface Feature API Sample](RuledSurfaceFeatureSample_Sample.md) | Demonstrates creating a new ruled surface feature. |

## Version

Introduced in version September 2020  

