# Sketch.redefine Method

Parent Object: [Sketch](Sketch.md)  

## Description

Changes which plane the sketch is based on.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.redefine(planarEntity)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntity | [Base](Base.md) | A construction plane or planar face that defines the sketch plane |

## Version

Introduced in version March 2016  

