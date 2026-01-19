# MachineLibrary.deleteAsset Method

Parent Object: [MachineLibrary](MachineLibrary.md)  

## Description

Delete asset by URL from the library. Throw an error if given URL does not point to a valid asset or the URL is read-only.

## Syntax

"machineLibrary_var" is a variable referencing a [MachineLibrary](MachineLibrary.md) object.

```python
returnValue = machineLibrary_var.deleteAsset(url)
```

## Return Value

| Type    | Description                                                     |
|---------|-----------------------------------------------------------------|
| boolean | Returns true if asset was deleted successfully, false otherwise |

## Parameters

| Name | Type           | Description                                  |
|------|----------------|----------------------------------------------|
| url  | [URL](URL.md) | The URL to the asset that should be removed. |

## Version

Introduced in version April 2023  

