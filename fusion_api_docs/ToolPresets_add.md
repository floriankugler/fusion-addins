# ToolPresets.add Method

Parent Object: [ToolPresets](ToolPresets.md)  

## Description

Creates and inserts a new Preset at the end of the Preset collection of the owning Tool. The new Preset will have the same values as the owning Tool.

## Syntax

"toolPresets_var" is a variable referencing a [ToolPresets](ToolPresets.md) object.

```python
returnValue = toolPresets_var.add()
```

## Return Value

| Type                         | Description                      |
|------------------------------|----------------------------------|
| [ToolPreset](ToolPreset.md) | Returns the newly created Preset |

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

