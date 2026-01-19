# ToolLibraries.urlByLocation Method

Parent Object: [ToolLibraries](ToolLibraries.md)  

## Description

Get the URL for a given LibraryLocations.

## Syntax

"toolLibraries_var" is a variable referencing a [ToolLibraries](ToolLibraries.md) object.

```python
returnValue = toolLibraries_var.urlByLocation(location)
```

## Return Value

| Type           | Description                         |
|----------------|-------------------------------------|
| [URL](URL.md) | Returns the URL for given location. |

## Parameters

| Name | Type | Description |
|----|----|----|
| location | [LibraryLocations](LibraryLocations.md) | The LibraryLocations to be converted into an URL. |

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

