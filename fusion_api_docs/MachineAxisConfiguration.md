# MachineAxisConfiguration Object

Derived from: [Base](Base.md) Object  

## Description

MachineAxisConfiguration holds controller settings that differ for each axis.

## Methods

| Name | Description |
|----|----|
| [classType](MachineAxisConfiguration_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](MachineAxisConfiguration_deleteMe.md) | Delete this axis configuration from the controller configuration. |

## Properties

| Name | Description |
| --- | --- |
| [coordinate](MachineAxisConfiguration_coordinate.md) | Coordinate to use for post processing. |
| [isReversed](MachineAxisConfiguration_isReversed.md) | Does the axis move in the opposite direction to usual. For rotary axes this would mean it uses the left hand rule, and for linear axes is moves in the opposite direction. |
| [isValid](MachineAxisConfiguration_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maxNormalSpeed](MachineAxisConfiguration_maxNormalSpeed.md) | Specifies the maximum normal speed for this axis. This would be called feedrate for a linear axis or rotary speed for a rotary axis. Units are cm/s for linear axes or rad/s for rotary axes. |
| [maxRapidSpeed](MachineAxisConfiguration_maxRapidSpeed.md) | Specifies the maximum rapid speed for this axis. This would be called feedrate for a linear axis or rotary speed for a rotary axis. Units are cm/s for linear axes or rad/s for rotary axes. |
| [objectType](MachineAxisConfiguration_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [partId](MachineAxisConfiguration_partId.md) | ID of the part in the KinematicsMachineElement that this axis configuration modifies. |
| [type](MachineAxisConfiguration_type.md) | The type of this axis configuration. Use this to inform a cast to the derived types. |

## Accessed From

[MachineAxisConfigurations.item](MachineAxisConfigurations_item.md), [MachineAxisConfigurations.itemById](MachineAxisConfigurations_itemById.md)

## Derived Classes

[LinearMachineAxisConfiguration](LinearMachineAxisConfiguration.md), [RotaryMachineAxisConfiguration](RotaryMachineAxisConfiguration.md)

## Version

Introduced in version April 2023  

