# JointOrigins.item Method

Parent Object: [JointOrigins](JointOrigins.md)  

## Description

Function that returns the specified joint origin using an index into the collection.

## Syntax

"jointOrigins_var" is a variable referencing a [JointOrigins](JointOrigins.md) object.

```python
returnValue = jointOrigins_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [JointOrigin](JointOrigin.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2015  

