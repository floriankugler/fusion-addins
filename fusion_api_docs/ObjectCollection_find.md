# ObjectCollection.find Method

Parent Object: [ObjectCollection](ObjectCollection.md)  

## Description

Finds the specified component in the collection.

## Syntax

"objectCollection_var" is a variable referencing an [ObjectCollection](ObjectCollection.md) object.

```python
# Uses no optional arguments.
returnValue = objectCollection_var.find(item)

# Uses optional arguments.
returnValue = objectCollection_var.find(item, startIndex)
```

## Return Value

| Type | Description |
|----|----|
| integer | Returns the index of the found item. If not found, -1 is returned. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| item | [Base](Base.md) | The item to search for within the collection. |
| startIndex | uinteger | The index to begin the search. This is an optional argument whose default value is 0. |

## Version

Introduced in version August 2014  

