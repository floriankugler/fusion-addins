# GenerateToolpathFuture.numberOfCompleted Property

Parent Object: [GenerateToolpathFuture](GenerateToolpathFuture.md)  

## Description

Returns the number of operations whose generation is complete.

## Syntax

"generateToolpathFuture_var" is a variable referencing a GenerateToolpathFuture object.  

```python
# Get the value of the property.
propertyValue = generateToolpathFuture_var.numberOfCompleted
```

## Property Value

This is a read only property whose value is an integer.

## Samples

| Name | Description |
| --- | --- |
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version January 2016  

