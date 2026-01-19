# Sketches.addToBaseOrFormFeature Method

Parent Object: [Sketches](Sketches.md)  

## Description

Creates a parametric sketch that is associated with a base feature.  

Because of a current limitation, if you want to create a sketch associated with a base feature, you must first call the edit method of the base feature, use this method to create the sketch, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it.

## Syntax

"sketches_var" is a variable referencing a [Sketches](Sketches.md) object.

```python
returnValue = sketches_var.addToBaseOrFormFeature(planarEntity, targetBaseOrFormFeature, includeFaceEdges)
```

## Return Value

| Type | Description |
|----|----|
| [Sketch](Sketch.md) | Returns the newly created Sketch or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntity | [Base](Base.md) | A construction plane or planar face that defines the sketch plane. |
| targetBaseOrFormFeature | [Base](Base.md) | The existing base feature that you want to associate this sketch with. |
| includeFaceEdges | boolean | When a BrepFace is used as the planarEntity argument, this defines if the edges of the face should be included in the sketch. |

## Samples

| Name | Description |
|----|----|
| [BaseFeature Sample](BaseFeatureSample_Sample.md) | Creates a new base feature. |
| [Sketches.addToBaseOrFormFeature](Sketches_addToFormBaseOrFeature_Sample.md) | Demonstrates the Sketches.addToBaseOrFormFeature method. |

## Version

Introduced in version May 2016  

