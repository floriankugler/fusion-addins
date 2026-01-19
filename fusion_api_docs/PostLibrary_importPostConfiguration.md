# PostLibrary.importPostConfiguration Method

Parent Object: [PostLibrary](PostLibrary.md)  

## Description

Import a given post configuration at a specific location. The post configuration will be stored in the library. Throws an error, if the given URL is read-only.

## Syntax

"postLibrary_var" is a variable referencing a [PostLibrary](PostLibrary.md) object.

```python
returnValue = postLibrary_var.importPostConfiguration(postConfig, destinationUrl, postName)
```

## Return Value

| Type | Description |
|----|----|
| [URL](URL.md) | Returns the URL of the newly imported post configuration, or null if the import failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| postConfig | [PostConfiguration](PostConfiguration.md) | The post configuration that should be imported. |
| destinationUrl | [URL](URL.md) | The URL to the folder where to save the post configuration. |
| postName | string | The name of the post configuration that should be created due to the import. The name can be extended if the name already exists at given location to ensure a unique name. |

## Samples

| Name | Description |
| --- | --- |
| [Basic Milling Workflow Sample](BasicMillingWorkflowSample_Sample.md) | Demonstrates the creation of a basic milling workflow from script Demonstrates creating a setup, searching tool library to retrieve a tool, create a couple of machining operations and a NC program, ready for post processing. Use the 2D Strategies model from the Fusion CAM Samples folder as your CAD model. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

