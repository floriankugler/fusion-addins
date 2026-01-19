
Derived from: [MultiAxisDPMFeedrateSettings](MultiAxisDPMFeedrateSettings.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Specialization of MultiAxisDPMFeedrateSettings for degrees per minute feedrates that require a combination of linear and rotary movements.

## Methods

| Name | Description |
|----|----|
| [classType](MultiAxisCombinationDPMFeedrateSettings_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [dpmType](MultiAxisCombinationDPMFeedrateSettings_dpmType.md) | The DPM settings type |
| [feedMode](MultiAxisCombinationDPMFeedrateSettings_feedMode.md) | The feedmode to use for the multi axis. |
| [isValid](MultiAxisCombinationDPMFeedrateSettings_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maximumFeedrate](MultiAxisCombinationDPMFeedrateSettings_maximumFeedrate.md) | The maximum feedrate value that can be output. |
| [objectType](MultiAxisCombinationDPMFeedrateSettings_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [outputTolerance](MultiAxisCombinationDPMFeedrateSettings_outputTolerance.md) | The tolerance for deciding whether to output a feedrate value or not. It helps to minimize the output of multi-axis feedrate numbers. If the feedrate value is within this tolerance of the previous feedrate value, then it is set to the previous value. Value is in deg/min. |
| [pulseWeight](MultiAxisCombinationDPMFeedrateSettings_pulseWeight.md) | The pulse weight ratio for the rotary axes when DPM feedrates are output as a combination of linear and rotary movements. The pulse weight is a scale factor based on the rotary axes accuracy compared to the linear axes accuracy. For example, it should be set to .1 when the linear axes are output on .0001 increments and the rotary axes on .001 increments. |

## Version

Introduced in version September 2025  

