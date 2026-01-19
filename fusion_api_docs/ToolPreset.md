# ToolPreset Object

Derived from: [Base](Base.md) Object  

## Description

A Preset defines the material specific properties of a Tool.

## Methods

| Name | Description |
|----|----|
| [classType](ToolPreset_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [id](ToolPreset_id.md) | Gets and sets the identifier of that Preset. The id can be used to select a Preset for a Operation. |
| [isValid](ToolPreset_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ToolPreset_name.md) | Gets and sets the name of that Preset. |
| [objectType](ToolPreset_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parameters](ToolPreset_parameters.md) | Gets the CAMParameters collection for this Preset. |

## Accessed From

[CAMTemplateOperationInput.toolPreset](CAMTemplateOperationInput_toolPreset.md), [Operation.toolPreset](Operation_toolPreset.md), [OperationInput.toolPreset](OperationInput_toolPreset.md), [ToolPresets.add](ToolPresets_add.md), [ToolPresets.item](ToolPresets_item.md), [ToolPresets.itemsByName](ToolPresets_itemsByName.md)

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

