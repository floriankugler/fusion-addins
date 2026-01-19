# PhysicalProperties.getPrincipalMomentsOfInertia Method

Parent Object: [PhysicalProperties](PhysicalProperties.md)  

## Description

Method that returns the moments of inertia about the principal axes. Unit for returned values is kg\*cm^2.

## Syntax

"physicalProperties_var" is a variable referencing a [PhysicalProperties](PhysicalProperties.md) object.  

```python
(returnValue, i1, i2, i3) = physicalProperties_var.getPrincipalMomentsOfInertia()
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
| [Get Physical Properties API Sample](GetPhysicalProperties_Sample.md) | Script that demonstrates getting physical properties using the API. When this script is run it will create a new document, build a simple model, and get the various physical properties from the model. |

## Version

Introduced in version May 2016  

