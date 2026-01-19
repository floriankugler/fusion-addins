# PostLibrary.childPostConfigurations Method

Parent Object: [PostLibrary](PostLibrary.md)  

## Description

Get all posts by the given parent folder URL. Returns null, if the URL does not exist.

## Syntax

"postLibrary_var" is a variable referencing a [PostLibrary](PostLibrary.md) object.

```python
returnValue = postLibrary_var.childPostConfigurations(url)
```

## Return Value

| Type | Description |
|----|----|
| [PostConfiguration](PostConfiguration.md)\[\] | Returns all children posts for a valid URL, returns null otherwise. |

## Parameters

| Name | Type           | Description                                            |
|------|----------------|--------------------------------------------------------|
| url  | [URL](URL.md) | The URL of the folder to get post configurations from. |

## Version

Introduced in version April 2023  

