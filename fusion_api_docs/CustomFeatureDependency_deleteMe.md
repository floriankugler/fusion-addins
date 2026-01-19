# CustomFeatureDependency.deleteMe Method

Parent Object: [CustomFeatureDependency](CustomFeatureDependency.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Deletes this dependency from the custom feature.

## Syntax

"customFeatureDependency_var" is a variable referencing a [CustomFeatureDependency](CustomFeatureDependency.md) object.

```python
returnValue = customFeatureDependency_var.deleteMe()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Version

Introduced in version January 2021  

