# TriadCommandInput.setFullVisibility Method

Parent Object: [TriadCommandInput](TriadCommandInput.md)  

## Description

A convenience method to turn on and off the visibility of commonly used controls in a triad. These include the X, Y, and Z axis translations, the X, Y, and Z axis rotations, scaling in the X, Y, and Z directions, scaling on the X-Y, Y-Z and Z-X planes, translation on the X-Y, Y-Z, and Z-X planes, and the origin move.

## Syntax

"triadCommandInput_var" is a variable referencing a [TriadCommandInput](TriadCommandInput.md) object.

```python
returnValue = triadCommandInput_var.setFullVisibility(isVisible)
```

## Return Value

| Type    | Description                        |
|---------|------------------------------------|
| boolean | Returns true if it was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| isVisible | boolean | Defines if the visibility of the controls should be turned on or off. True indicates they will be visible. |

## Version

Introduced in version May 2022  

