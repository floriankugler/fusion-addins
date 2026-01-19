# SelectionSets.itemByName Method

Parent Object: [SelectionSets](SelectionSets.md)  

## Description

Returns the specified SelectionSet object using the name of the selection set.

## Syntax

"selectionSets_var" is a variable referencing a [SelectionSets](SelectionSets.md) object.

```python
returnValue = selectionSets_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [SelectionSet](SelectionSet.md) | Returns the specified SelectionSet object or null if no SelectionSet object exists with the specified name. |

## Parameters

| Name | Type   | Description                                    |
|------|--------|------------------------------------------------|
| name | string | The name of the SelectionSet object to return. |

## Version

Introduced in version May 2022  

