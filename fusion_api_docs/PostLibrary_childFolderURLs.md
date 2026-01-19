# PostLibrary.childFolderURLs Method

Parent Object: [PostLibrary](PostLibrary.md)  

## Description

Get all library folders under given URL.

## Syntax

"postLibrary_var" is a variable referencing a [PostLibrary](PostLibrary.md) object.

```python
returnValue = postLibrary_var.childFolderURLs(url)
```

## Return Value

| Type               | Description                                    |
|--------------------|------------------------------------------------|
| [URL](URL.md)\[\] | Returns list of folder URLs at given location. |

## Parameters

| Name | Type           | Description                   |
|------|----------------|-------------------------------|
| url  | [URL](URL.md) | The URL to the parent folder. |

## Version

Introduced in version April 2023  

