# UserParameters.exportUserParameters Method

Parent Object: [UserParameters](UserParameters.md)  

## Description

Function that exports a list of user parameters to a csv file.

## Syntax

"userParameters_var" is a variable referencing a [UserParameters](UserParameters.md) object.

```python
returnValue = userParameters_var.exportUserParameters(userParameterArray, filename)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns whether the export was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| userParameterArray | UserParameter\[\] | The array of user parameters to export. |
| filename | string | The full filename (path and file) of the file to write the parameters to. |

## Version

Introduced in version September 2024  

