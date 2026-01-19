# AsBuiltJointList.itemByName Method

Parent Object: [AsBuiltJointList](AsBuiltJointList.md)  

## Description

Function that returns the specified as-built joint using a name.

## Syntax

"asBuiltJointList_var" is a variable referencing an [AsBuiltJointList](AsBuiltJointList.md) object.

```python
returnValue = asBuiltJointList_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [AsBuiltJoint](AsBuiltJoint.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                     |
|------|--------|-------------------------------------------------|
| name | string | The name of the item within the list to return. |

## Version

Introduced in version January 2016  

