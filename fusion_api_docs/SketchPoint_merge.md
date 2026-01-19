# SketchPoint.merge Method

Parent Object: [SketchPoint](SketchPoint.md)  

## Description

Merges the input sketch point into this sketch point. This effectively deletes the other sketch point and changes all entities that referenced that sketch point to reference this sketch point.  

This is the equivalent of dragging a sketch point on top of another sketch point in the user interface.

## Syntax

"sketchPoint_var" is a variable referencing a [SketchPoint](SketchPoint.md) object.

```python
returnValue = sketchPoint_var.merge(point)
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| boolean | Returns true if the merge was successful. |

## Parameters

| Name  | Type                           | Description                         |
|-------|--------------------------------|-------------------------------------|
| point | [SketchPoint](SketchPoint.md) | The point to merge with this point. |

## Version

Introduced in version August 2014  

