# ToolLibraries.updateToolLibrary Method

Parent Object: [ToolLibraries](ToolLibraries.md)  

## Description

Update ToolLibrary in ToolLibraries. Overrides the URL by given ToolLibrary. Throws an error if the URL does not already point to an existing ToolLibrary.

## Syntax

"toolLibraries_var" is a variable referencing a [ToolLibraries](ToolLibraries.md) object.

```python
returnValue = toolLibraries_var.updateToolLibrary(url, toolLibrary)
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns true if asset was updated successfully, false otherwise. |

## Parameters

| Name | Type | Description |
|----|----|----|
| url | [URL](URL.md) | The URL to the existing asset in the ToolLibraries that should be updated. |
| toolLibrary | [ToolLibrary](ToolLibrary.md) | The ToolLibrary that should be persisted. |

## Version

Introduced in version April 2023  

