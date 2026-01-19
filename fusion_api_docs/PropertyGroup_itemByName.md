# PropertyGroup.itemByName Method

Parent Object: [PropertyGroup](PropertyGroup.md)  

## Description

Returns the specified Property using the name of the property.

## Syntax

"propertyGroup_var" is a variable referencing a [PropertyGroup](PropertyGroup.md) object.

```python
returnValue = propertyGroup_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Property](Property.md) | Returns the specified property or null if the name doesn't match a property within the group. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the property to return. This is the name as seen in the user interface and may be localized. |

## Version

Introduced in version January 2024  

