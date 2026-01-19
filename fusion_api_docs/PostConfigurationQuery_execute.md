# PostConfigurationQuery.execute Method

Parent Object: [PostConfigurationQuery](PostConfigurationQuery.md)  

## Description

Query for specific posts. This PostConfiguration query.

## Syntax

"postConfigurationQuery_var" is a variable referencing a [PostConfigurationQuery](PostConfigurationQuery.md) object.

```python
returnValue = postConfigurationQuery_var.execute()
```

## Return Value

| Type | Description |
|----|----|
| [PostConfiguration](PostConfiguration.md)\[\] | Returns a list of posts. Each returned post matches this query. |

## Samples

| Name | Description |
| --- | --- |
| [Basic Milling Workflow Sample](BasicMillingWorkflowSample_Sample.md) | Demonstrates the creation of a basic milling workflow from script Demonstrates creating a setup, searching tool library to retrieve a tool, create a couple of machining operations and a NC program, ready for post processing. Use the 2D Strategies model from the Fusion CAM Samples folder as your CAD model. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version May 2023  

