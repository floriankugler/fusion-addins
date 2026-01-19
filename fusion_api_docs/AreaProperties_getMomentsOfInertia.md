# AreaProperties.getMomentsOfInertia Method

Parent Object: [AreaProperties](AreaProperties.md)  

## Description

Method that, for a sketch, returns the moments of inertia about the sketch origin. For a planar face, this method returns the moments about the world coordinate system origin. Unit for returned values is kg\*cm^2.

## Syntax

"areaProperties_var" is a variable referencing an [AreaProperties](AreaProperties.md) object.  

```python
(returnValue, ixx, iyy, izz, ixy, iyz, ixz) = areaProperties_var.getMomentsOfInertia()
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type   | Description                                       |
|------|--------|---------------------------------------------------|
| ixx  | double | Output Double that returns the XX partial moment. |
| iyy  | double | Output Double that returns the YY partial moment. |
| izz  | double | Output Double that returns the ZZ partial moment. |
| ixy  | double | Output Double that returns the XY partial moment. |
| iyz  | double | Output Double that returns the YZ partial moment. |
| ixz  | double | Output Double that returns the XZ partial moment. |

## Samples

| Name | Description |
|----|----|
| [API Sample for AreaProperties](AreaPropertiesSample_Sample.md) | Demonstrates how to use AreaProperties |

## Version

Introduced in version March 2016  

