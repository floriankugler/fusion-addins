# Component.sketches Property

Parent Object: [Component](Component.md)  

## Description

Returns the sketches collection associated with this component. This provides access to the existing sketches and supports the creation of new sketches.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.sketches
```

## Property Value

This is a read only property whose value is a [Sketches](Sketches.md).

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |
| [Sketches.add](Sketches_add_Sample.md) | Demonstrates the Sketches.add method. |
| [Sketches.addToBaseOrFormFeature](Sketches_addToFormBaseOrFeature_Sample.md) | Demonstrates the Sketches.addToBaseOrFormFeature method. |

## Version

Introduced in version August 2014  

