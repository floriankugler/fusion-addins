# CAMLibrary.doesPathExist Method

Parent Object: [CAMLibrary](CAMLibrary.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Checks if the given URL points to an existing folder or asset in the library.

## Syntax

"cAMLibrary_var" is a variable referencing a [CAMLibrary](CAMLibrary.md) object.

```python
returnValue = cAMLibrary_var.doesPathExist(url)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the URL points to an existing folder or asset, false otherwise. |

## Parameters

| Name | Type           | Description            |
|------|----------------|------------------------|
| url  | [URL](URL.md) | The URL to be checked. |

## Version

Introduced in version September 2025  

