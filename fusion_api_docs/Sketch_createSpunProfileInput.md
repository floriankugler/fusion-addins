# Sketch.createSpunProfileInput Method

Parent Object: [Sketch](Sketch.md)  

## Description

Creates a new SpunProfileInput object that is used to specify the input needed to create a spun profile.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.createSpunProfileInput(entities, axis)
```

## Return Value

| Type | Description |
|----|----|
| [SpunProfileInput](SpunProfileInput.md) | Returns the newly created SpunProfileInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | Base\[\] | An array containing the entities (BRepBody or BRepFace) to create a spun profile. |
| axis | [Base](Base.md) | The axis can be a sketch line, construction axis, or linear edge. The axis must not be perpendicular to the sketch plane. |

## Version

Introduced in version November 2024  

