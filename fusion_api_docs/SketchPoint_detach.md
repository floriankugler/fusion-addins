# SketchPoint.detach Method

Parent Object: [SketchPoint](SketchPoint.md)  

## Description

This method disconnects the specified curve from the sketch point. The specified curve must use this point as one of its endpoints, and at least one other sketch curve must also use the point as its endpoint. Detaching the curve creates a new sketch point, which becomes the curve's end point. All other curves using the original sketch point will remain unaffected.

## Syntax

"sketchPoint_var" is a variable referencing a [SketchPoint](SketchPoint.md) object.

```python
returnValue = sketchPoint_var.detach(curve)
```

## Return Value

| Type | Description |
|----|----|
| [SketchPoint](SketchPoint.md) | If successful, the newly created sketch point that the curve was moved to is returned. Null is returned in the case of failure. Typical failure cases are if the specified curve is the only curve connected to the point or if the curve is not connected to the point. |

## Parameters

| Name | Type | Description |
|----|----|----|
| curve | [SketchCurve](SketchCurve.md) | The sketch curve to detach from the sketch point. One of its end points must be the sketch point. |

## Version

Introduced in version March 2025  

