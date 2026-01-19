# CutPasteBodies.add Method

Parent Object: [CutPasteBodies](CutPasteBodies.md)  

## Description

Cuts and copies the specified body into the component that owns this CutPasteBodies collection. This is effectively the equivalent of moving a body.

## Syntax

"cutPasteBodies_var" is a variable referencing a [CutPasteBodies](CutPasteBodies.md) object.

```python
returnValue = cutPasteBodies_var.add(sourceBody)
```

## Return Value

| Type | Description |
|----|----|
| [CutPasteBody](CutPasteBody.md) | Returns the newly created BRepBody object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sourceBody | [Base](Base.md) | Either an ObjectCollection of BRepBodies or a single BRepBody object to cut. |

## Version

Introduced in version June 2017  

