# ConstructionPlaneInput.setByPlane Method

Parent Object: [ConstructionPlaneInput](ConstructionPlaneInput.md)  

## Description

This input method is for creating a non-parametric construction plane positioned in space as defined by the input Plane object.  

This method of defining a construction plane is only valid when working in the direct modeling mode. This is not valid when working in the parametric modeling mode and will fail.

## Syntax

"constructionPlaneInput_var" is a variable referencing a [ConstructionPlaneInput](ConstructionPlaneInput.md) object.

```python
returnValue = constructionPlaneInput_var.setByPlane(plane)
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns true if the construction plane definition is successful. |

## Parameters

| Name  | Type               | Description              |
|-------|--------------------|--------------------------|
| plane | [Plane](Plane.md) | A transient plane object |

## Version

Introduced in version August 2014  

