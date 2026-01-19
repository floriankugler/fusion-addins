# PhysicalProperties.getRadiusOfGyration Method

Parent Object: [PhysicalProperties](PhysicalProperties.md)  

## Description

Method that returns the radius of gyration about the principal axes. Unit for returned values is cm.

## Syntax

"physicalProperties_var" is a variable referencing a [PhysicalProperties](PhysicalProperties.md) object.  

```python
(returnValue, kx, ky, kz) = physicalProperties_var.getRadiusOfGyration()
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type   | Description                                                  |
|------|--------|--------------------------------------------------------------|
| kx   | double | Output Double that returns the X partial radius of gyration. |
| ky   | double | Output Double that returns the Y partial radius of gyration. |
| kz   | double | Output Double that returns the Z partial radius of gyration. |

## Samples

| Name | Description |
|----|----|
| [Get Physical Properties API Sample](GetPhysicalProperties_Sample.md) | Script that demonstrates getting physical properties using the API. When this script is run it will create a new document, build a simple model, and get the various physical properties from the model. |

## Version

Introduced in version May 2016  

