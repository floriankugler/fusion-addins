# Sketches.item Method

Parent Object: [Sketches](Sketches.md)  

## Description

Function that returns the specified sketch using an index into the collection.

## Syntax

"sketches_var" is a variable referencing a [Sketches](Sketches.md) object.

```python
returnValue = sketches_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Sketch](Sketch.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

