# GeometricConstraints.addParallel Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new parallel constraint between two lines.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addParallel(lineOne, lineTwo)
```

## Return Value

| Type | Description |
|----|----|
| [ParallelConstraint](ParallelConstraint.md) | Returns the newly created ParallelConstraint object or null if the creation failed. |

## Parameters

| Name    | Type                         | Description            |
|---------|------------------------------|------------------------|
| lineOne | [SketchLine](SketchLine.md) | The first SketchLine.  |
| lineTwo | [SketchLine](SketchLine.md) | The second SketchLine. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraints.addParallel](GeometricConstraints_addParallel_Sample.md) | Demonstrate the GeometricConstraints.addParallel method. |

## Version

Introduced in version August 2014  

