# CAM.generateAllToolpaths Method

Parent Object: [CAM](CAM.md)  

## Description

Generates or regenerates all the operations in the document, including those nested in sub-folders or patterns.

## Syntax

"cAM_var" is a variable referencing a [CAM](CAM.md) object.

```python
returnValue = cAM_var.generateAllToolpaths(skipValid)
```

## Return Value

| Type | Description |
|----|----|
| [GenerateToolpathFuture](GenerateToolpathFuture.md) | Return GenerateToolpathFuture that includes the status of operation generation. |

## Parameters

| Name | Type | Description |
|----|----|----|
| skipValid | boolean | Option to skip valid operations and only regenerate invalid operations. |

## Samples

| Name | Description |
|----|----|
| [CAM Parameter Modification API Sample](CAMParameterChange_Sample_Sample.md) | Demonstrates changing parameters of existing toolpaths. |
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |
| [Create CAM Operation From Template API Sample](New_Operation_Sample_Sample.md) | Demonstrates adding a new toolpath into the document using an existing CAM template. You can view the template [here](../ExtraFiles/face.f3dhsm-template), although it will be loaded automatically. Run the sample script within any Fusion project containing at least one setup. A new facing operation will be created at the end of each setup discovered. |

## Version

Introduced in version January 2016  

