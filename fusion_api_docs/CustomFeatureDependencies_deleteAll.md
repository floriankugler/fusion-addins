# CustomFeatureDependencies.deleteAll Method

Parent Object: [CustomFeatureDependencies](CustomFeatureDependencies.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Deletes all of the current dependencies. This method is for convenience and is equivalent to iterating through the collection and deleting them one at a time.

## Syntax

"customFeatureDependencies_var" is a variable referencing a [CustomFeatureDependencies](CustomFeatureDependencies.md) object.

```python
returnValue = customFeatureDependencies_var.deleteAll()
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Version

Introduced in version August 2021  

