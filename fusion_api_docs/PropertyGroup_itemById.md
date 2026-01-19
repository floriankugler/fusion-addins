# PropertyGroup.itemById Method

Parent Object: [PropertyGroup](PropertyGroup.md)  

## Description

Returns the specified property from the group using the unique ID of the property. The ID is consistent and can't be modified by the user and isn't affected by localization.

## Syntax

"propertyGroup_var" is a variable referencing a [PropertyGroup](PropertyGroup.md) object.

```python
returnValue = propertyGroup_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [Property](Property.md) | Returns the specified Property or null if the ID doesn't match a property within the collection. |

## Parameters

| Name | Type   | Description                    |
|------|--------|--------------------------------|
| id   | string | The unique ID of the property. |

## Version

Introduced in version January 2024  

