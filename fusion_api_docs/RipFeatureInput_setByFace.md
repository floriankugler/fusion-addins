# RipFeatureInput.setByFace Method

Parent Object: [RipFeatureInput](RipFeatureInput.md)  

## Description

Specifies the rip feature will be defined by a face..

## Syntax

"ripFeatureInput_var" is a variable referencing a [RipFeatureInput](RipFeatureInput.md) object.

```python
returnValue = ripFeatureInput_var.setByFace(face)
```

## Return Value

| Type    | Description                                         |
|---------|-----------------------------------------------------|
| boolean | Returns true if the defining the rip is successful. |

## Parameters

| Name | Type                     | Description                                |
|------|--------------------------|--------------------------------------------|
| face | [BRepFace](BRepFace.md) | The sheet metal face that defines the rip. |

## Version

Introduced in version September 2023  

