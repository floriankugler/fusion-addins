# PostConfigurationQuery.capability Property

Parent Object: [PostConfigurationQuery](PostConfigurationQuery.md)  

## Description

Specifies the capability to search for in the post library.

## Syntax

"postConfigurationQuery_var" is a variable referencing a PostConfigurationQuery object.  

```python
# Get the value of the property.
propertyValue = postConfigurationQuery_var.capability

# Set the value of the property.
postConfigurationQuery_var.capability = propertyValue
```

## Property Value

This is a read/write property whose value is a [PostCapabilities](PostCapabilities.md).

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

