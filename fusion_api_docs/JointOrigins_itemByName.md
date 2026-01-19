# JointOrigins.itemByName Method

Parent Object: [JointOrigins](JointOrigins.md)  

## Description

Function that returns the specified joint origin using a name.

## Syntax

"jointOrigins_var" is a variable referencing a [JointOrigins](JointOrigins.md) object.

```python
returnValue = jointOrigins_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [JointOrigin](JointOrigin.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                           |
|------|--------|-------------------------------------------------------|
| name | string | The name of the item within the collection to return. |

## Version

Introduced in version September 2015  

