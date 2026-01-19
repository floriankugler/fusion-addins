# MeshFeature.deleteMe Method

Parent Object: [MeshFeature](MeshFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Deletes the feature. This works for both parametric and non-parametric features.

## Syntax

"meshFeature_var" is a variable referencing a [MeshFeature](MeshFeature.md) object.

```python
returnValue = meshFeature_var.deleteMe()
```

## Return Value

| Type    | Description                                                    |
|---------|----------------------------------------------------------------|
| boolean | Returns a bool indicating if the delete was successful or not. |

## Version

Introduced in version March 2024  

