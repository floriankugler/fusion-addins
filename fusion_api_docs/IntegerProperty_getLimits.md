# IntegerProperty.getLimits Method

Parent Object: [IntegerProperty](IntegerProperty.md)  

## Description

Method that returns any limits for the value of this property. The HasLimits property can be used to see if there are any limits or not.  

This is most commonly used for properties associated with materials and appearances.

## Syntax

"integerProperty_var" is a variable referencing an [IntegerProperty](IntegerProperty.md) object.  

```python
(returnValue, hasLowLimit, lowLimit, hasHighLimit, highLimit) = integerProperty_var.getLimits()
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if the method call was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| hasLowLimit | boolean | Output Boolean that indicates if there is a low limit or not. |
| lowLimit | integer | If the hasLowLimit argument is true, this argument returns the low limit. |
| hasHighLimit | boolean | Output Boolean that indicates if there is a high limit or not. |
| highLimit | integer | If the hasHighLimit argument is true, this argument returns the high limit. |

## Version

Introduced in version August 2014  

