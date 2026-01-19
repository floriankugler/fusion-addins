# MotionLinkInput.valueOne Property

Parent Object: [MotionLinkInput](MotionLinkInput.md)  

## Description

Gets and sets the first motion link value. If the ValueInput uses a real then it is interpreted as centimeters for length and radians for angle. If it is a string then the units can be defined as part of the string (i.e. "2 in" or "60 deg") or if no units are specified it is interpreted using the current default units for length or angle.

## Syntax

"motionLinkInput_var" is a variable referencing a MotionLinkInput object.  

```python
# Get the value of the property.
propertyValue = motionLinkInput_var.valueOne

# Set the value of the property.
motionLinkInput_var.valueOne = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version November 2025  

