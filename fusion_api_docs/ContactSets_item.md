# ContactSets.item Method

Parent Object: [ContactSets](ContactSets.md)  

## Description

Returns the specified contact set using an index into the collection.

## Syntax

"contactSets_var" is a variable referencing a [ContactSets](ContactSets.md) object.

```python
returnValue = contactSets_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ContactSet](ContactSet.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2016  

