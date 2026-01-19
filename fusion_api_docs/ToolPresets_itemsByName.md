# ToolPresets.itemsByName Method

Parent Object: [ToolPresets](ToolPresets.md)  

## Description

Search presets by name. Returns all presets for which the name matches the given pattern. Compare is case insensitive and characters \* and ? are used for wild-card matching.

## Syntax

"toolPresets_var" is a variable referencing a [ToolPresets](ToolPresets.md) object.

```python
returnValue = toolPresets_var.itemsByName(name)
```

## Return Value

| Type                             | Description                             |
|----------------------------------|-----------------------------------------|
| [ToolPreset](ToolPreset.md)\[\] | Returns all presets with matching name. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | Name of the Preset to search for. The string can define a pattern with wild-card matching. '\*' represents an arbitrary sequence including the empty sequence and '?' represents one arbitrary character. |

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

