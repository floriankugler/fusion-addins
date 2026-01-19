# JointList.itemByName Method

Parent Object: [JointList](JointList.md)  

## Description

Function that returns the specified joint using a name.

## Syntax

"jointList_var" is a variable referencing a [JointList](JointList.md) object.

```python
returnValue = jointList_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Joint](Joint.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                     |
|------|--------|-------------------------------------------------|
| name | string | The name of the item within the list to return. |

## Version

Introduced in version January 2016  

