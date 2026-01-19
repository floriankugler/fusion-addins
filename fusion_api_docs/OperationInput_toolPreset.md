# OperationInput.toolPreset Property

Parent Object: [OperationInput](OperationInput.md)  

## Description

Optionally specify the preset of the tool. If no preset is specified, the operation gets its default feed and speed. The Tool provides access to available presets. Use one of those presets to override the default. Setting the tool will overwrite a subset of tool parameters in the parameters property. An invalid preset will cause a failure during the creation of the operation.

## Syntax

"operationInput_var" is a variable referencing an OperationInput object.  

```python
# Get the value of the property.
propertyValue = operationInput_var.toolPreset

# Set the value of the property.
operationInput_var.toolPreset = propertyValue
```

## Property Value

This is a read/write property whose value is a [ToolPreset](ToolPreset.md).

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

