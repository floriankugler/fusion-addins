# CopyPasteBodies.add Method

Parent Object: [CopyPasteBodies](CopyPasteBodies.md)  

## Description

Copies the specified body into the component that owns this CopyPasteBodies collection.

## Syntax

"copyPasteBodies_var" is a variable referencing a [CopyPasteBodies](CopyPasteBodies.md) object.

```python
returnValue = copyPasteBodies_var.add(sourceBody)
```

## Return Value

| Type | Description |
|----|----|
| [CopyPasteBody](CopyPasteBody.md) | Returns the newly created BRepBody object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sourceBody | [Base](Base.md) | Either an ObjectCollection of BRepBodies or a single BRepBody object to copy. |

## Version

Introduced in version June 2017  

