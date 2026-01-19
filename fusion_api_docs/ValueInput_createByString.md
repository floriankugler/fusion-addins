# ValueInput.createByString Method

Parent Object: [ValueInput](ValueInput.md)  

## Description

When a string is used to create a value it needs to be evaluated as an expression so its value can be determined using the UnitsManager class. The units of an expression can be explicitly defined or will default to the current default units. For example, if you create an expression with the string "6" and specify it as a length, it will use the current active units. If the current active units are defined as inches the expression will be interpreted as 6 inches. You can specify the units as part of the string (i.e. "6 mm"). You can also use equations in the string (i.e. "6 + 5mm")  

In order for an expression to be valid, its units must be compatible with the value it represents. For example if you specify "5 in + 3 cm" as an expression to supply the value of an angle, it will fail because the units of the expression define a length.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.ValueInput.createByString(stringValue)
```

## Return Value

| Type | Description |
|----|----|
| [ValueInput](ValueInput.md) | Returns the newly created ValueInput object or null if the creation failed. |

## Parameters

| Name        | Type   | Description           |
|-------------|--------|-----------------------|
| stringValue | string | The expression string |

## Samples

| Name | Description |
|----|----|
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version August 2014  

