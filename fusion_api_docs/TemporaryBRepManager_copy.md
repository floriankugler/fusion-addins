# TemporaryBRepManager.copy Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Creates a temporary copy of the input BRepBody, BRepFace, or BRepEdge object.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.copy(bRepEntity)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns a BRepBody that contains the result. If a BRepBody is input the copy is of the entire body. If a BRepFace is input, then the result is a BRepBody that contains a single face. If a BRepLoop is input then the result is a BRepBody that contains a wire where each edge in the loop will have a corresponding edge in the wire. If a BRepEdge is input then the result is a BRepBody that contains a wire that contains the single edge. |

## Parameters

| Name | Type | Description |
|----|----|----|
| bRepEntity | [Base](Base.md) | The BRepBody, BRepFace, BRepLoop, or BRepEdge to create a copy of. This can be a parametric B-Rep entity or a temporary B-Rep entity. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

