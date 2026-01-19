# TSplineBodies.addByTSMDescription Method

Parent Object: [TSplineBodies](TSplineBodies.md)  

## Description

Creates a new TSplineBody using the T-Spline description provided by the input string which contains TSM formatted text.

## Syntax

"tSplineBodies_var" is a variable referencing a [TSplineBodies](TSplineBodies.md) object.

```python
returnValue = tSplineBodies_var.addByTSMDescription(tsmDescription)
```

## Return Value

| Type | Description |
|----|----|
| [TSplineBody](TSplineBody.md) | Returns the newly created TSplineBody if successful or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| tsmDescription | string | A string that contains a T-Spline description in TSM form. |

## Version

Introduced in version April 2019  

