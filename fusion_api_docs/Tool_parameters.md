# Tool.parameters Property

Parent Object: [Tool](Tool.md)  

## Description

Gets the CAMParameters collection associated with this tool. This defines all of the settings that describe the details of the tool.

## Syntax

"tool_var" is a variable referencing a Tool object.  

```python
# Get the value of the property.
propertyValue = tool_var.parameters
```

## Property Value

This is a read only property whose value is a [CAMParameters](CAMParameters.md).

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

