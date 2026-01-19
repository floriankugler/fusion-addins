# PropertyGroups.itemByName Method

Parent Object: [PropertyGroups](PropertyGroups.md)  

## Description

Returns the specified PropertyGroup using the name of the group.

## Syntax

"propertyGroups_var" is a variable referencing a [PropertyGroups](PropertyGroups.md) object.

```python
returnValue = propertyGroups_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [PropertyGroup](PropertyGroup.md) | Returns the specified group or null if the name doesn't match a group within the collection. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the group to return. This is the name as seen in the user interface. Not all groups have a name. |

## Version

Introduced in version January 2024  

