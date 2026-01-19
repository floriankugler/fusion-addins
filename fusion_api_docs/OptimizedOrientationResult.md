# OptimizedOrientationResult Object

Derived from: [Base](Base.md) Object  

## Description

The orientation result instance. Contains properties that can be used to create a custom ranking and the orientation matrix. The calculated ranking is based on the orientation operation's ranking priorities.

## Methods

| Name | Description |
|----|----|
| [classType](OptimizedOrientationResult_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [boundingBoxVolume](OptimizedOrientationResult_boundingBoxVolume.md) | The volume of the bounding box aligned to the world coordinate system of the oriented part. The value is given in cubic centimeters |
| [centerOfGravityHeight](OptimizedOrientationResult_centerOfGravityHeight.md) | The height of the center of gravity of the oriented part. The value is given in centimeters |
| [isValid](OptimizedOrientationResult_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](OptimizedOrientationResult_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [partHeight](OptimizedOrientationResult_partHeight.md) | The resulting height of the oriented part. The value is given in centimeters |
| [rankingValue](OptimizedOrientationResult_rankingValue.md) | The value which the initial ordering is based on. Calculated based on the properties above by the orientation operation. |
| [supportArea](OptimizedOrientationResult_supportArea.md) | The shadow area of the support hull below the oriented part. The value is given in squared centimeters |
| [supportVolume](OptimizedOrientationResult_supportVolume.md) | The volume of the support hull below the oriented part. The value is given in cubic centimeters |
| [transformation](OptimizedOrientationResult_transformation.md) | The transformation matrix to be applied onto the occurrence's existing transformation at the time of the calculation. |

## Accessed From

[OptimizedOrientationResults.currentOrientationResult](OptimizedOrientationResults_currentOrientationResult.md), [OptimizedOrientationResults.initialOrientationResult](OptimizedOrientationResults_initialOrientationResult.md), [OptimizedOrientationResults.item](OptimizedOrientationResults_item.md)

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing FFF API Sample](AdditiveFFFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive FFF manufacturing setup and generate a toolpath. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select an FFF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected FFF machine. This script will also create support structures, if required, based on the orientation of each component. Finally, the script generates the toolpath for the active setup and lets the user choose if they wish to post process the resulting toolpath or if they want to simulate it. |
| [Additive Manufacturing SLA API Sample](AdditiveSLAManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive SLA manufacturing setup. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select a SLA 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected SLA machine. This script will also create support structures, based on the orientation of each component. The support and orientation operations are created from a template. The script further demonstrates how to wrap script code into a command such that only one undo entry is created for the entire script instead of one entry per internal action. |

## Version

Introduced in version July 2023  

