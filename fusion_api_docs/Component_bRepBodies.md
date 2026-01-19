# Component.bRepBodies Property

Parent Object: [Component](Component.md)  

## Description

Returns the B-Rep bodies collection associated with this component.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.bRepBodies
```

## Property Value

This is a read only property whose value is a [BRepBodies](BRepBodies.md).

## Samples

| Name | Description |
|----|----|
| [Get Volume of Active Design API Sample](GetsVolumeOfActiveDesign_Sample.md) | Traverses through the active design and totals the volume of every body within the design. |

## Version

Introduced in version August 2014  

