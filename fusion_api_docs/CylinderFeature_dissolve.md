# CylinderFeature.dissolve Method

Parent Object: [CylinderFeature](CylinderFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"cylinderFeature_var" is a variable referencing a [CylinderFeature](CylinderFeature.md) object.

```python
returnValue = cylinderFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version September 2015  

