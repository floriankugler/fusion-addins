# Tool.presets Property

Parent Object: [Tool](Tool.md)  

## Description

Gets the ToolPresets collection associated with this tool.

## Syntax

"tool_var" is a variable referencing a Tool object.  

```python
# Get the value of the property.
propertyValue = tool_var.presets
```

## Property Value

This is a read only property whose value is a [ToolPresets](ToolPresets.md).

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

