# RotaryMachineAxisInput.rotationAxis Property

Parent Object: [RotaryMachineAxisInput](RotaryMachineAxisInput.md)  

## Description

The infinite line that defines the direction and location of the axis of rotation. This direction is in the machine's coordinate system (e.g. an A axis would typically use (1,0,0) for the direction), and follows the right-hand rule.

## Syntax

"rotaryMachineAxisInput_var" is a variable referencing a RotaryMachineAxisInput object.  

```python
# Get the value of the property.
propertyValue = rotaryMachineAxisInput_var.rotationAxis

# Set the value of the property.
rotaryMachineAxisInput_var.rotationAxis = propertyValue
```

## Property Value

This is a read/write property whose value is an [InfiniteLine3D](InfiniteLine3D.md).

## Version

Introduced in version April 2023  

