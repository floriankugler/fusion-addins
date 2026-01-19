# Snapshots.item Method

Parent Object: [Snapshots](Snapshots.md)  

## Description

Function that returns the specified snapshot in the collection using an index into the collection.

## Syntax

"snapshots_var" is a variable referencing a [Snapshots](Snapshots.md) object.

```python
returnValue = snapshots_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Snapshot](Snapshot.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

