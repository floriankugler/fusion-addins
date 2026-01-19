# JointOriginList.itemByName Method

Parent Object: [JointOriginList](JointOriginList.md)  

## Description

Function that returns the specified joint origin using a name.

## Syntax

"jointOriginList_var" is a variable referencing a [JointOriginList](JointOriginList.md) object.

```python
returnValue = jointOriginList_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [JointOrigin](JointOrigin.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                     |
|------|--------|-------------------------------------------------|
| name | string | The name of the item within the list to return. |

## Version

Introduced in version January 2016  

