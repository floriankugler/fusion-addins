# Tool Object

Derived from: [Base](Base.md) Object  

## Description

Represents a Tool.

## Methods

| Name | Description |
|----|----|
| [classType](Tool_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createFromJson](Tool_createFromJson.md) | Creates a Tool object from given JSON string. |
| [createFromP21](Tool_createFromP21.md) | Creates a Tool object given a string containing a tool defined using the P21 format. Throws an error if the given string does not conform to the P21 format. |
| [toJson](Tool_toJson.md) | Generates and returns a JSON string that contains a description of this tool. |

## Properties

| Name | Description |
| --- | --- |
| [description](Tool_description.md) | Gets the descriptive text about the tool. Includes various pieces of information depending on the tool type. Usually contains the tool number, data describing the tool geometry and the description. In the UI, the same information is displayed in the operation tree or in the tool library table. |
| [isValid](Tool_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Tool_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parameters](Tool_parameters.md) | Gets the CAMParameters collection associated with this tool. This defines all of the settings that describe the details of the tool. |
| [presets](Tool_presets.md) | Gets the ToolPresets collection associated with this tool. |

## Accessed From

[CAMTemplateOperationInput.tool](CAMTemplateOperationInput_tool.md), [DocumentToolLibrary.item](DocumentToolLibrary_item.md), [DocumentToolLibrary.toolsBySetupOrFolder](DocumentToolLibrary_toolsBySetupOrFolder.md), [Operation.tool](Operation_tool.md), [OperationInput.tool](OperationInput_tool.md), [Tool.createFromJson](Tool_createFromJson.md), [Tool.createFromP21](Tool_createFromP21.md), [ToolLibrary.item](ToolLibrary_item.md), [ToolQueryResult.tool](ToolQueryResult_tool.md)

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

