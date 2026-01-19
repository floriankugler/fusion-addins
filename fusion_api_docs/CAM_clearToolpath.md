# CAM.clearToolpath Method

Parent Object: [CAM](CAM.md)  

## Description

Clears all the toolpaths for the specified objects, including those nested in sub-folders or patterns.

## Syntax

"cAM_var" is a variable referencing a [CAM](CAM.md) object.

```python
returnValue = cAM_var.clearToolpath(operations)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Return true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| operations | [Base](Base.md) | An Operation, Setup, Folder, or Pattern object. You can also use and ObjectCollection to specify multiple objects of any combination of types. |

## Version

Introduced in version January 2016  

