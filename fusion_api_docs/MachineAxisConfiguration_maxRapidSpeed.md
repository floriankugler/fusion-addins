# MachineAxisConfiguration.maxRapidSpeed Property

Parent Object: [MachineAxisConfiguration](MachineAxisConfiguration.md)  

## Description

Specifies the maximum rapid speed for this axis. This would be called feedrate for a linear axis or rotary speed for a rotary axis. Units are cm/s for linear axes or rad/s for rotary axes.

## Syntax

"machineAxisConfiguration_var" is a variable referencing a MachineAxisConfiguration object.  

```python
# Get the value of the property.
propertyValue = machineAxisConfiguration_var.maxRapidSpeed

# Set the value of the property.
machineAxisConfiguration_var.maxRapidSpeed = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version April 2023  

