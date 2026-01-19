# CAMParameters Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to the parameters of an existing operation.

## Methods

| Name | Description |
|----|----|
| [classType](CAMParameters_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](CAMParameters_item.md) | Function that returns the specified parameter using an index into the collection. |
| [itemByName](CAMParameters_itemByName.md) | Returns the parameter of the specified id (internal name). |
| [resetToSystemDefaults](CAMParameters_resetToSystemDefaults.md) | Resets each parameter to its system default. |

## Properties

| Name | Description |
| --- | --- |
| [count](CAMParameters_count.md) | The number of items in the collection. |
| [isValid](CAMParameters_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CAMParameters_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMAdditiveContainer.parameters](CAMAdditiveContainer_parameters.md), [CAMFolder.parameters](CAMFolder_parameters.md), [CAMHoleRecognition.parameters](CAMHoleRecognition_parameters.md), [CAMPattern.parameters](CAMPattern_parameters.md), [CAMTemplateOperationInput.parameters](CAMTemplateOperationInput_parameters.md), [NCProgram.parameters](NCProgram_parameters.md), [NCProgram.postParameters](NCProgram_postParameters.md), [NCProgramInput.parameters](NCProgramInput_parameters.md), [Operation.parameters](Operation_parameters.md), [OperationBase.parameters](OperationBase_parameters.md), [OperationInput.parameters](OperationInput_parameters.md), [PostProcessingMachineElement.postParameters](PostProcessingMachineElement_postParameters.md), [PrintSetting.parameters](PrintSetting_parameters.md), [PrintSettingItem.parameters](PrintSettingItem_parameters.md), [Setup.parameters](Setup_parameters.md), [SetupInput.parameters](SetupInput_parameters.md), [Tool.parameters](Tool_parameters.md), [ToolPreset.parameters](ToolPreset_parameters.md)

## Samples

| Name | Description |
| --- | --- |
| [CAM Parameter Modification API Sample](CAMParameterChange_Sample_Sample.md) | Demonstrates changing parameters of existing toolpaths. |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version September 2020  

