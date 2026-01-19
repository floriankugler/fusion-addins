# DataFile.move Method

Parent Object: [DataFile](DataFile.md)  

## Description

Moves this DataFile to the specified folder.

## Syntax

"dataFile_var" is a variable referencing a [DataFile](DataFile.md) object.

```python
returnValue = dataFile_var.move(targetFolder)
```

## Return Value

| Type    | Description                              |
|---------|------------------------------------------|
| boolean | Returns true if the move was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| targetFolder | [DataFolder](DataFolder.md) | The folder to move this DataFile to. |

## Version

Introduced in version September 2016  

