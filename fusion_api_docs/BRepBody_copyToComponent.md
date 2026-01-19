# BRepBody.copyToComponent Method

Parent Object: [BRepBody](BRepBody.md)  

## Description

Creates a copy of this body into the specified target.

## Syntax

"bRepBody_var" is a variable referencing a [BRepBody](BRepBody.md) object.

```python
returnValue = bRepBody_var.copyToComponent(target)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the moved BRepBody or null in the case the move failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| target | [Base](Base.md) | The target can be either the root component or an occurrence. In the case where an occurrence is specified, the body will be copied into the parent component of the target occurrence and the target occurrence defines the transform of how the body will be copied so that the body maintains it's same position with respect to the assembly. If target is null, then a copy of the body is created in the owning component of the original body. |

## Version

Introduced in version June 2015  

