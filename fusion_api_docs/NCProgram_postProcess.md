# NCProgram.postProcess Method

Parent Object: [NCProgram](NCProgram.md)  

## Description

Creates machine-specific NC code for this NC program.

## Syntax

"nCProgram_var" is a variable referencing a [NCProgram](NCProgram.md) object.

```python
returnValue = nCProgram_var.postProcess(options)
```

## Return Value

| Type    | Description                                      |
|---------|--------------------------------------------------|
| boolean | Returns true if the post process was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| options | [NCProgramPostProcessOptions](NCProgramPostProcessOptions.md) | NCProgramPostProcessOptions to speficy the behavior on internal warning. Can be null if the default values should be used. If needed it can be created by its static create() method. |

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

