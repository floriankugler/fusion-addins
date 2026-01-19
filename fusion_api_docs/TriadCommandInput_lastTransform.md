# TriadCommandInput.lastTransform Property

Parent Object: [TriadCommandInput](TriadCommandInput.md)  

## Description

Returns the transform of the triad before the latest change. Using the matrices returned by this property and the transform property you can determine what changed. The lastChangeMade property is also useful to help you know the type of change to look for when comparing the matrices.

## Syntax

"triadCommandInput_var" is a variable referencing a TriadCommandInput object.  

```python
# Get the value of the property.
propertyValue = triadCommandInput_var.lastTransform
```

## Property Value

This is a read only property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version May 2022  

