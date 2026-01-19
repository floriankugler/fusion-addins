# UserParameters.importUserParameters Method

Parent Object: [UserParameters](UserParameters.md)  

## Description

Function that imports a list of user parameters from a csv file.  

The format of the csv file is as follows: It must have at least two rows - Header followed by a row of parameter. It must be encoded in UTF8 format. It must contain at least six columns - name, unit, expression, value, comment, and favorite where favorite is either true or false. The columns must only have a comma delimiter. Any locale will work but no thousands. expression column support double quotes. comment can either be single line or multi line. If multi line, it must be in double quotes.  

Here is an example of a csv file with two rows Name,Unit,Expression,Value,Comments,Favorite p1,mm,32 mm,32,the first parameter,FALSE  

The function exportUserParameters could be used to see what a csv file looks like.

## Syntax

"userParameters_var" is a variable referencing a [UserParameters](UserParameters.md) object.

```python
returnValue = userParameters_var.importUserParameters(filename)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns whether the import was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filename | string | The full filename (path and file) of the file to read the parameters from. |

## Version

Introduced in version September 2024  

