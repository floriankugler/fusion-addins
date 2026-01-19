# TSplineBodies.addByTSMFile Method

Parent Object: [TSplineBodies](TSplineBodies.md)  

## Description

Creates a new TSplineBody by reading in a TSM file from disk.

## Syntax

"tSplineBodies_var" is a variable referencing a [TSplineBodies](TSplineBodies.md) object.

```python
returnValue = tSplineBodies_var.addByTSMFile(tsmFilename)
```

## Return Value

| Type | Description |
|----|----|
| [TSplineBody](TSplineBody.md) | Returns the newly created TSplineBody if successful or null in the case of failure. |

## Parameters

| Name        | Type   | Description                                |
|-------------|--------|--------------------------------------------|
| tsmFilename | string | The full filename of the TSM file on disk. |

## Version

Introduced in version April 2019  

