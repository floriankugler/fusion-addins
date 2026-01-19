# NCProgramPostProcessOptions.create Method

Parent Object: [NCProgramPostProcessOptions](NCProgramPostProcessOptions.md)  

## Description

Creates a new NCProgramPostProcessOptions object to be used as an input argument by the postProcess() method.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.NCProgramPostProcessOptions.create()
```

## Return Value

| Type | Description |
|----|----|
| [NCProgramPostProcessOptions](NCProgramPostProcessOptions.md) | Returns the newly created NCProgramPostProcessOptions object or null if the creation failed. |

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version May 2023  

