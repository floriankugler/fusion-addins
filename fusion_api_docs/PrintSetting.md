# PrintSetting Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a PrintSetting.

## Methods

| Name | Description |
|----|----|
| [classType](PrintSetting_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createFromXML](PrintSetting_createFromXML.md) | Creates a PrintSetting from a xml content. |
| [deletePrintSettingItem](PrintSetting_deletePrintSettingItem.md) | Deletes the PrintSettingItem of the specified body preset. Throws an exception when the name does not match any available PrintSettingItems or when trying to delete the default PrintSettingItem. |
| [duplicatePrintSettingItem](PrintSetting_duplicatePrintSettingItem.md) | Duplicates the PrintSetting item of the specified body preset. |
| [getDefaultPrintSettingItem](PrintSetting_getDefaultPrintSettingItem.md) | Gets the default PrintSetting item of the specified body preset. Throws exception when name not found. |
| [isCompatibleWithMachine](PrintSetting_isCompatibleWithMachine.md) | Checks whether the print setting is usable with the given machine. |
| [item](PrintSetting_item.md) | Get the PrintSettingItem at index in PrintSetting. |
| [itemByName](PrintSetting_itemByName.md) | Returns the PrintSetting item of the specified body preset. |
| [parameters](PrintSetting_parameters.md) | Function that returns the specified parameterTable using an enum into the collection. |
| [setDefaultPrintSettingItem](PrintSetting_setDefaultPrintSettingItem.md) | Defaults the PrintSetting item of the specified body preset. Throws exception when name not found. |
| [syncWithMachine](PrintSetting_syncWithMachine.md) | Synchronizes the print setting with the given machine, making extruder parameter options dependent on the available extruders in the machine. |
| [toXML](PrintSetting_toXML.md) | Generates and returns the print setting xml content string. |

## Properties

| Name | Description |
| --- | --- |
| [count](PrintSetting_count.md) | Get the number of PrintSettingItems in this collection. |
| [description](PrintSetting_description.md) | Gets and sets the description of the PrintSetting. |
| [id](PrintSetting_id.md) | Gets the unique identifier of the PrintSetting. Can be used for comparing PrintSettings within the document. |
| [isValid](PrintSetting_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](PrintSetting_name.md) | Gets and sets the name of the PrintSetting. |
| [objectType](PrintSetting_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [technology](PrintSetting_technology.md) | Gets the technology of the PrintSetting. |

## Accessed From

[PrintSetting.createFromXML](PrintSetting_createFromXML.md), [PrintSettingLibrary.childPrintSettings](PrintSettingLibrary_childPrintSettings.md), [PrintSettingLibrary.printSettingAtURL](PrintSettingLibrary_printSettingAtURL.md), [PrintSettingQuery.execute](PrintSettingQuery_execute.md), [Setup.printSetting](Setup_printSetting.md), [SetupInput.printSetting](SetupInput_printSetting.md)

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing FFF API Sample](AdditiveFFFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive FFF manufacturing setup and generate a toolpath. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select an FFF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected FFF machine. This script will also create support structures, if required, based on the orientation of each component. Finally, the script generates the toolpath for the active setup and lets the user choose if they wish to post process the resulting toolpath or if they want to simulate it. |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |
| [Additive Manufacturing SLA API Sample](AdditiveSLAManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive SLA manufacturing setup. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select a SLA 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected SLA machine. This script will also create support structures, based on the orientation of each component. The support and orientation operations are created from a template. The script further demonstrates how to wrap script code into a command such that only one undo entry is created for the entire script instead of one entry per internal action. |

## Version

Introduced in version April 2023  

