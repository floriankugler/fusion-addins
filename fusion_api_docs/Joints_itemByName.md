# Joints.itemByName Method

Parent Object: [Joints](Joints.md)  

## Description

Function that returns the specified joint using a name.

## Syntax

"joints_var" is a variable referencing a [Joints](Joints.md) object.

```python
returnValue = joints_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Joint](Joint.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                           |
|------|--------|-------------------------------------------------------|
| name | string | The name of the item within the collection to return. |

## Version

Introduced in version September 2015  

