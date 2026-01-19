# NCProgramInput.displayName Property

Parent Object: [NCProgramInput](NCProgramInput.md)  

## Description

Optionally specify the display name that appears in the browser-tree to override the default.

## Syntax

"nCProgramInput_var" is a variable referencing a NCProgramInput object.  

```python
# Get the value of the property.
propertyValue = nCProgramInput_var.displayName

# Set the value of the property.
nCProgramInput_var.displayName = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

