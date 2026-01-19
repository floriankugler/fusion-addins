# PostLibrary.displayName Method

Parent Object: [PostLibrary](PostLibrary.md)  

## Description

Get the localized display name for a given URL. The URL must point to a folder.

## Syntax

"postLibrary_var" is a variable referencing a [PostLibrary](PostLibrary.md) object.

```python
returnValue = postLibrary_var.displayName(url)
```

## Return Value

| Type | Description |
|----|----|
| string | Returns localized display name for the folder. Returns empty string for invalid URL. |

## Parameters

| Name | Type           | Description                                |
|------|----------------|--------------------------------------------|
| url  | [URL](URL.md) | The URL that defines the path to a folder. |

## Version

Introduced in version April 2023  

