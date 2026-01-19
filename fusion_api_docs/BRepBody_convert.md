# BRepBody.convert Method

Parent Object: [BRepBody](BRepBody.md)  

## Description

Creates a new body where the faces and edges are converted to different types of geometry based on the input options. This is particularly useful when you need a body made up entirely of NURBS surfaces.  

The tempId on the faces, edges, and vertices on the new body will match with the corresponding tempId on the original body. In cases where faces are split as a result of the conversion there can be more than one face or edge in the new body that matches to a single face or edge in the original body. The findByTempId method will find the entity with the matching id.

## Syntax

"bRepBody_var" is a variable referencing a [BRepBody](BRepBody.md) object.

```python
returnValue = bRepBody_var.convert(options)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the new converted body or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| options | [BRepConvertOptions](BRepConvertOptions.md) | Input options that define how the conversion should be done. These are bitwise options so they can be combined. |

## Version

Introduced in version August 2016  

