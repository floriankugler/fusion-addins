# CustomGraphicsGroup.item Method

Parent Object: [CustomGraphicsGroup](CustomGraphicsGroup.md)  

## Description

Function that returns the specified custom graphics entity within this group. This also includes any child graphics groups.

## Syntax

"customGraphicsGroup_var" is a variable referencing a [CustomGraphicsGroup](CustomGraphicsGroup.md) object.

```python
returnValue = customGraphicsGroup_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsEntity](CustomGraphicsEntity.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2017  

