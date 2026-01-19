# TSplineBodies.itemByName Method

Parent Object: [TSplineBodies](TSplineBodies.md)  

## Description

Returns a TSplineBody by specifying the name of the body as seen in the browser.

## Syntax

"tSplineBodies_var" is a variable referencing a [TSplineBodies](TSplineBodies.md) object.

```python
returnValue = tSplineBodies_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [TSplineBody](TSplineBody.md) | Returns the specified item or null if a body with that name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the body, as seen in the browser. This is case sensitive. |

## Version

Introduced in version April 2019  

