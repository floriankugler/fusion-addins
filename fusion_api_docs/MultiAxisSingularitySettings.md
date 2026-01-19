
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Base class for multi-axis singularity settings.

## Methods

| Name | Description |
|----|----|
| [classType](MultiAxisSingularitySettings_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createLinearizationSettings](MultiAxisSingularitySettings_createLinearizationSettings.md) | Creates a MultiAxisSingularityLinearizationSettings object. Set this object on the linearizationSettings property to apply the changes. |

## Properties

| Name | Description |
| --- | --- |
| [angle](MultiAxisSingularitySettings_angle.md) | The minimum angular delta movement for the rotary axes before the singularity is adjusted. When fluctuations of the rotary axes are insignificant, this limit prevents adjustment of the tool axis vector. Typically set to 10 degrees or more. Value is in radians. |
| [cone](MultiAxisSingularitySettings_cone.md) | The angular distance range between the tool axis vector and the singularity point before the singularity is adjusted. Typically, the angular distance is less than 5 degrees. The further the tool axis is from the singularity, the less visible the fluctuations in the rotary axes are. Value is in radians. |
| [isValid](MultiAxisSingularitySettings_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [linearizationSettings](MultiAxisSingularitySettings_linearizationSettings.md) | The settings for linearization of moves around the singularity. See MultiAxisSingularityLinearizeMethod for more details. Set this to null to not use linearization. For changes to to this object to take effect, re-assign them to this property. |
| [objectType](MultiAxisSingularitySettings_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [tolerance](MultiAxisSingularitySettings_tolerance.md) | The tolerance value for converting simultaneous multi-axis movements to linear movements when the tool axis is near a singularity. |

## Accessed From

[MultiAxisMachineElement.createSingularitySettings](MultiAxisMachineElement_createSingularitySettings.md), [MultiAxisMachineElement.singularitySettings](MultiAxisMachineElement_singularitySettings.md)

## Version

Introduced in version September 2025  

