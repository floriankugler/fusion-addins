# MotionLinks.item Method

Parent Object: [MotionLinks](MotionLinks.md)  

## Description

Function that returns the specified MotionLink using an index into the collection.

## Syntax

"motionLinks_var" is a variable referencing a [MotionLinks](MotionLinks.md) object.

```python
returnValue = motionLinks_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [MotionLink](MotionLink.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2025  

