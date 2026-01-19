# AsBuiltJoints.itemByName Method

Parent Object: [AsBuiltJoints](AsBuiltJoints.md)  

## Description

Function that returns the specified as-built joint using a name.

## Syntax

"asBuiltJoints_var" is a variable referencing an [AsBuiltJoints](AsBuiltJoints.md) object.

```python
returnValue = asBuiltJoints_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [AsBuiltJoint](AsBuiltJoint.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                           |
|------|--------|-------------------------------------------------------|
| name | string | The name of the item within the collection to return. |

## Version

Introduced in version September 2015  

