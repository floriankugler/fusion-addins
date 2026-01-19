# ToolLibraries.childAssetURLs Method

Parent Object: [ToolLibraries](ToolLibraries.md)  

## Description

Get all assets under given URL.

## Syntax

"toolLibraries_var" is a variable referencing a [ToolLibraries](ToolLibraries.md) object.

```python
returnValue = toolLibraries_var.childAssetURLs(url)
```

## Return Value

| Type               | Description                                   |
|--------------------|-----------------------------------------------|
| [URL](URL.md)\[\] | Returns list of asset URLs at given location. |

## Parameters

| Name | Type           | Description                   |
|------|----------------|-------------------------------|
| url  | [URL](URL.md) | The URL to the parent folder. |

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

