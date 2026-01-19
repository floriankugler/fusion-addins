# CAM.checkToolpath Method

Parent Object: [CAM](CAM.md)  

## Description

Checks if the operations (including those nested in sub-folders or patterns) are valid and up to date.

## Syntax

"cAM_var" is a variable referencing a [CAM](CAM.md) object.

```python
returnValue = cAM_var.checkToolpath(operations)
```

## Return Value

| Type    | Description                              |
|---------|------------------------------------------|
| boolean | Returns true if the operations are valid |

## Parameters

| Name | Type | Description |
|----|----|----|
| operations | [Base](Base.md) | An Operation, Setup, Folder, or Pattern object. You can also use an ObjectCollection to specify multiple objects of any of the supported types. |

## Version

Introduced in version January 2016  

