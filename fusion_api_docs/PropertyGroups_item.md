# PropertyGroups.item Method

Parent Object: [PropertyGroups](PropertyGroups.md)  

## Description

Returns the specified property group from the collection using an index into the collection.

## Syntax

"propertyGroups_var" is a variable referencing a [PropertyGroups](PropertyGroups.md) object.

```python
returnValue = propertyGroups_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [PropertyGroup](PropertyGroup.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the property within the collection where the first item is 0. |

## Version

Introduced in version January 2024  

