# MotionLinks.add Method

Parent Object: [MotionLinks](MotionLinks.md)  

## Description

Creates a new MotionLink.

## Syntax

"motionLinks_var" is a variable referencing a [MotionLinks](MotionLinks.md) object.

```python
returnValue = motionLinks_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [MotionLink](MotionLink.md) | Returns the newly created MotionLink or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [MotionLinkInput](MotionLinkInput.md) | The MotionLinkInput object that defines various inputs that fully define a MotionLink. A MotionLinkInput object is created using the MotionLinks.createInput method. |

## Version

Introduced in version November 2025  

