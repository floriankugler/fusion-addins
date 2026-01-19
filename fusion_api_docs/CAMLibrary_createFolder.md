# CAMLibrary.createFolder Method

Parent Object: [CAMLibrary](CAMLibrary.md)  

## Description

Create a new folder in the library. Create the folder under given parent URL with given folder name. Add counting suffix, in case a folder with given name already exists. Throw an error if given URL does not point to a valid folder or the URL is read-only. Also throws an error if given folder name is empty.

## Syntax

"cAMLibrary_var" is a variable referencing a [CAMLibrary](CAMLibrary.md) object.

```python
returnValue = cAMLibrary_var.createFolder(parentUrl, folderName)
```

## Return Value

| Type           | Description                                 |
|----------------|---------------------------------------------|
| [URL](URL.md) | Returns the URL to the newly created folder |

## Parameters

| Name | Type | Description |
|----|----|----|
| parentUrl | [URL](URL.md) | The parent URL for the folder to be created. |
| folderName | string | Name of the new folder to be created. Must not be empty. |

## Version

Introduced in version May 2023  

