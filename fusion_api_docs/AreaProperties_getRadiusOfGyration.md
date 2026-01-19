# AreaProperties.getRadiusOfGyration Method

Parent Object: [AreaProperties](AreaProperties.md)  

## Description

Method that returns the radius of gyration about the principal axes. Unit for returned values is cm.

## Syntax

"areaProperties_var" is a variable referencing an [AreaProperties](AreaProperties.md) object.  

```python
(returnValue, kxx, kyy, kzz) = areaProperties_var.getRadiusOfGyration()
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type   | Description                                                  |
|------|--------|--------------------------------------------------------------|
| kxx  | double | Output Double that returns the X partial radius of gyration. |
| kyy  | double | Output Double that returns the Y partial radius of gyration. |
| kzz  | double | Output Double that returns the Z partial radius of gyration. |

## Samples

| Name | Description |
|----|----|
| [API Sample for AreaProperties](AreaPropertiesSample_Sample.md) | Demonstrates how to use AreaProperties |

## Version

Introduced in version March 2016  

