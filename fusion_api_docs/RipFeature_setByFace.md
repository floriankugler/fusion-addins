# RipFeature.setByFace Method

Parent Object: [RipFeature](RipFeature.md)  

## Description

This input method is for creating a rip from a face.

## Syntax

"ripFeature_var" is a variable referencing a [RipFeature](RipFeature.md) object.

```python
returnValue = ripFeature_var.setByFace(face)
```

## Return Value

| Type    | Description                                       |
|---------|---------------------------------------------------|
| boolean | Returns true if the rip definition is successful. |

## Parameters

| Name | Type                     | Description                                |
|------|--------------------------|--------------------------------------------|
| face | [BRepFace](BRepFace.md) | The sheet metal face that defines the rip. |

## Version

Introduced in version September 2023  

