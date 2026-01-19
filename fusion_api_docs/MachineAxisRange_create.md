# MachineAxisRange.create Method

Parent Object: [MachineAxisRange](MachineAxisRange.md)  

## Description

Creates a new range object with limited extents. Requires min to be less than or equal to max. Types of the fields depend on where this range is being used. Centimeters are used for distances and radians for angles.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.MachineAxisRange.create(min, max)
```

## Return Value

| Type | Description |
|----|----|
| [MachineAxisRange](MachineAxisRange.md) | A new range object. Returns null if validation fails. |

## Parameters

| Name | Type   | Description                  |
|------|--------|------------------------------|
| min  | double | New minimum value for range. |
| max  | double | New maximum value for range. |

## Version

Introduced in version April 2023  

