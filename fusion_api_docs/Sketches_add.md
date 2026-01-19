# Sketches.add Method

Parent Object: [Sketches](Sketches.md)  

## Description

Creates a new sketch on the specified planar entity.

## Syntax

"sketches_var" is a variable referencing a [Sketches](Sketches.md) object.

```python
# Uses no optional arguments.
returnValue = sketches_var.add(planarEntity)

# Uses optional arguments.
returnValue = sketches_var.add(planarEntity, occurrenceForCreation)
```

## Return Value

| Type | Description |
|----|----|
| [Sketch](Sketch.md) | Returns the newly created Sketch or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| planarEntity | [Base](Base.md) | A construction plane or planar face that defines the sketch plane |
| occurrenceForCreation | [Occurrence](Occurrence.md) | A creation occurrence is needed if the planarEntity is in another component AND the sketch is not in the root component. The occurrenceForCreation is analogous to the active occurrence in the UI. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |
| [Sketches.add](Sketches_add_Sample.md) | Demonstrates the Sketches.add method. |

## Version

Introduced in version August 2014  

