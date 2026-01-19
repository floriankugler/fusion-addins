# FusionUnitsManager.evaluateExpression Method

Parent Object: [FusionUnitsManager](FusionUnitsManager.md)  

## Description

Gets the value (in internal units) of the expression.

## Syntax

"fusionUnitsManager_var" is a variable referencing a [FusionUnitsManager](FusionUnitsManager.md) object.

```python
# Uses no optional arguments.
returnValue = fusionUnitsManager_var.evaluateExpression(expression)

# Uses optional arguments.
returnValue = fusionUnitsManager_var.evaluateExpression(expression, units)
```

## Return Value

| Type | Description |
|----|----|
| double | Returns -1 AND GetLastError will return ExpressionError in the event of an error. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| expression | string | EvaluateExpression("1cm + 1in") -> 3.54 EvaluateExpression("1") -> -> depends on the DistanceUnits, with "mm" it gives 0.1 |
| units | string | If not supplied the units will default to the default length specified in the preferences. This is an optional argument whose default value is "DefaultDistance". |

## Version

Introduced in version August 2014  

