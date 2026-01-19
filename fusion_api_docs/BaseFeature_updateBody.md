# BaseFeature.updateBody Method

Parent Object: [BaseFeature](BaseFeature.md)  

## Description

Update an existing source BRepBody created by this BaseFeature. The input BRepBody definition will be copied into the existing BRepBody.

## Syntax

"baseFeature_var" is a variable referencing a [BaseFeature](BaseFeature.md) object.

```python
returnValue = baseFeature_var.updateBody(sourceBody, newBody)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the body was updated, or false if the update failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sourceBody | [BRepBody](BRepBody.md) | The source BRepBody to update. The source bodies of a BaseFeature are only available from the bodies collection of the BaseFeature when the BaseFeature is in edit mode. |
| newBody | [BRepBody](BRepBody.md) | The BRepBody whose definition will be used to replace the existing source body's definition. |

## Version

Introduced in version January 2021  

