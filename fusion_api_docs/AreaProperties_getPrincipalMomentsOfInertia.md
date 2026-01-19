# AreaProperties.getPrincipalMomentsOfInertia Method

Parent Object: [AreaProperties](AreaProperties.md)  

## Description

Method that returns the moments of inertia about the principal axes. Unit for returned values is kg\*cm^2.

## Syntax

"areaProperties_var" is a variable referencing an [AreaProperties](AreaProperties.md) object.  

```python
(returnValue, i1, i2, i3) = areaProperties_var.getPrincipalMomentsOfInertia()
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type   | Description                                                |
|------|--------|------------------------------------------------------------|
| i1   | double | Output Double that specifies the first moment of inertia.  |
| i2   | double | Output Double that specifies the second moment of inertia. |
| i3   | double | Output Double that specifies the third moment of inertia.  |

## Samples

| Name | Description |
|----|----|
| [API Sample for AreaProperties](AreaPropertiesSample_Sample.md) | Demonstrates how to use AreaProperties |

## Version

Introduced in version March 2016  

