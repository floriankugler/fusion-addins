# ToolPreset.parameters Property

Parent Object: [ToolPreset](ToolPreset.md)  

## Description

Gets the CAMParameters collection for this Preset.

## Syntax

"toolPreset_var" is a variable referencing a ToolPreset object.  

```python
# Get the value of the property.
propertyValue = toolPreset_var.parameters
```

## Property Value

This is a read only property whose value is a [CAMParameters](CAMParameters.md).

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

