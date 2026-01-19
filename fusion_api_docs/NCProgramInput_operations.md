# NCProgramInput.operations Property

Parent Object: [NCProgramInput](NCProgramInput.md)  

## Description

Gets and sets the operations which will be included in the NC program. Valid input contains any number of operations, setups or folders. For setups and folders all child operations will be added. Operations will be post processed in setup order, with operations from the same setup grouped together. Setting the nc_program_orderByTool BooleanParameterValue on the parameters property to true will reorder operations across multiple setups to reduce the number of tool changes. When the list of operations is associated to one setup and the setup has defined its job_programName or job_programComment parameters, then those values are applied to the nc_program_name and nc_program_comment parameters accordingly.

## Syntax

"nCProgramInput_var" is a variable referencing a NCProgramInput object.  

```python
# Get the value of the property.
propertyValue = nCProgramInput_var.operations

# Set the value of the property.
nCProgramInput_var.operations = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [OperationBase](OperationBase.md).

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

