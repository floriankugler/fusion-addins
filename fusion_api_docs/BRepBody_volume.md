# BRepBody.volume Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

Returns the volume in cm ^ 3. Returns 0 in the case the body is not solid.

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.volume
```

## Property Value

This is a read only property whose value is a double.

## Samples

| Name | Description |
|----|----|
| [Get Volume of Active Design API Sample](GetsVolumeOfActiveDesign_Sample.md) | Traverses through the active design and totals the volume of every body within the design. |

## Version

Introduced in version August 2014  

