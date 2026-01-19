# ObjectCollection.removeByIndex Method

Parent Object: [ObjectCollection](ObjectCollection.md)  

## Description

Function that removes an item from the list. Will fail if the list is read only.

## Syntax

"objectCollection_var" is a variable referencing an [ObjectCollection](ObjectCollection.md) object.

```python
returnValue = objectCollection_var.removeByIndex(index)
```

## Return Value

| Type    | Description                                 |
|---------|---------------------------------------------|
| boolean | Returns true if the removal was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item to remove from the collection. The first item has an index of 0. |

## Version

Introduced in version August 2014  

