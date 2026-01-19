# CAM.postProcessAll Method

Parent Object: [CAM](CAM.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Post all of the toolpaths (includes those nested in sub-folders or patterns) in the document. If post processing fails, an error message can be retrieved from the error log explaining the reason for the failure.

## Syntax

"cAM_var" is a variable referencing a [CAM](CAM.md) object.

```python
returnValue = cAM_var.postProcessAll(input)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [PostProcessInput](PostProcessInput.md) | The PostProcessInput object that defines the post options and parameters. |

## Samples

| Name | Description |
|----|----|
| [Post Toolpaths API Sample](PostToolpaths_Sample_Sample.md) | Demonstrates posting toolpaths in the active document. |

## Version

Introduced in version January 2016  
Retired in version September 2025  

