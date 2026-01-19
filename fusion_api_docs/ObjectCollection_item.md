# ObjectCollection.item Method

Parent Object: [ObjectCollection](ObjectCollection.md)  

## Description

Function that returns the specified object using an index into the collection.

## Syntax

"objectCollection_var" is a variable referencing an [ObjectCollection](ObjectCollection.md) object.

```python
returnValue = objectCollection_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Base](Base.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

