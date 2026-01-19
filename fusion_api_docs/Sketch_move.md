# Sketch.move Method

Parent Object: [Sketch](Sketch.md)  

## Description

Moves the specified sketch entities using the specified transform. Transform respects any constraints that would normally prohibit the move.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.move(sketchEntities, transform)
```

## Return Value

| Type    | Description                              |
|---------|------------------------------------------|
| boolean | Returns true if the move was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sketchEntities | [ObjectCollection](ObjectCollection.md) | A collection of sketch entities to transform. |
| transform | [Matrix3D](Matrix3D.md) | The transform that defines the move, rotate or scale. |

## Version

Introduced in version August 2014  

