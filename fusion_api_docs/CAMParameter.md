# CAMParameter Object

Derived from: [Base](Base.md) Object  

## Description

Base class for representing parameter of an operation.

## Methods

| Name | Description |
|----|----|
| [classType](CAMParameter_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [saveExpressionAsUserDefault](CAMParameter_saveExpressionAsUserDefault.md) | Saves the current expression as user default value. Throws an exception if the parent is not an operation or does not support user default expressions. |

## Properties

| Name | Description |
| --- | --- |
| [error](CAMParameter_error.md) | Returns a message corresponding to any active error associated with the value of this parameter. |
| [expression](CAMParameter_expression.md) | Gets and sets the value expression of the parameter. |
| [fullTitle](CAMParameter_fullTitle.md) | Returns the full title of this parameter as seen in the user interface. This can potentially be more descriptive than the basic title. This title is localized and can change based on the current language. |
| [isDeprecated](CAMParameter_isDeprecated.md) | Gets if this parameter is deprecated. Some parameters are deprecated when their usage becomes obsolete. Reading deprecated parameters is allowed, but setting deprecated parameters will throw an error. |
| [isEditable](CAMParameter_isEditable.md) | Returns whether or not the parameter's expression or value can be modified. |
| [isEnabled](CAMParameter_isEnabled.md) | Gets if this parameter is enabled. Some parameters are enabled/disabled depending on the values set for other parameters. |
| [isValid](CAMParameter_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](CAMParameter_isVisible.md) | Gets if this parameter is visible in the user interface. |
| [name](CAMParameter_name.md) | Gets the name (internal name) of the parameter. |
| [objectType](CAMParameter_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [systemDefaultExpression](CAMParameter_systemDefaultExpression.md) | Returns the systemDefaultExpression of this parameter. |
| [title](CAMParameter_title.md) | Returns the title of this parameter as seen in the user interface. This title is localized and can change based on the current language |
| [userDefaultExpression](CAMParameter_userDefaultExpression.md) | Gets and sets the userDefaultExpression of this parameter. If no userDefaultExpression is set, the systemDefaultExpression is returned. Throws an exception if the parent is not an operation or does not support user default expressions. |
| [value](CAMParameter_value.md) | Returns an object that allows you to get and set the value associated with the parameter. |
| [warning](CAMParameter_warning.md) | Returns a message corresponding to any active warning associated with the value of this parameter. |

## Accessed From

[CAMParameters.item](CAMParameters_item.md), [CAMParameters.itemByName](CAMParameters_itemByName.md)

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing FFF API Sample](AdditiveFFFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive FFF manufacturing setup and generate a toolpath. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select an FFF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected FFF machine. This script will also create support structures, if required, based on the orientation of each component. Finally, the script generates the toolpath for the active setup and lets the user choose if they wish to post process the resulting toolpath or if they want to simulate it. |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |
| [Additive Manufacturing SLA API Sample](AdditiveSLAManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive SLA manufacturing setup. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select a SLA 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected SLA machine. This script will also create support structures, based on the orientation of each component. The support and orientation operations are created from a template. The script further demonstrates how to wrap script code into a command such that only one undo entry is created for the entire script instead of one entry per internal action. |
| [CAM Parameter Modification API Sample](CAMParameterChange_Sample_Sample.md) | Demonstrates changing parameters of existing toolpaths. |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |

## Version

Introduced in version September 2020  

