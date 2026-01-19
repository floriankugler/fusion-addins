# TemporaryBRepManager.transform Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Transforms the input body using the specified transformation matrix.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.transform(body, transform)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the specified transform was successfully applied to the body. |

## Parameters

| Name | Type | Description |
|----|----|----|
| body | [BRepBody](BRepBody.md) | The BRepBody object to transform. |
| transform | [Matrix3D](Matrix3D.md) | The transformation matrix that defines the transform to apply to the body. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

