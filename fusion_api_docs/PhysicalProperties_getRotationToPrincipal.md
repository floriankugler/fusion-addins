# PhysicalProperties.getRotationToPrincipal Method

Parent Object: [PhysicalProperties](PhysicalProperties.md)  

## Description

Gets the rotation from the world coordinate system of the target to the principal coordinate system.

## Syntax

"physicalProperties_var" is a variable referencing a [PhysicalProperties](PhysicalProperties.md) object.  

```python
(returnValue, rx, ry, rz) = physicalProperties_var.getRotationToPrincipal()
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type   | Description |
|------|--------|-------------|
| rx   | double |             |
| ry   | double |             |
| rz   | double |             |

## Samples

| Name | Description |
|----|----|
| [Get Physical Properties API Sample](GetPhysicalProperties_Sample.md) | Script that demonstrates getting physical properties using the API. When this script is run it will create a new document, build a simple model, and get the various physical properties from the model. |

## Version

Introduced in version May 2016  

