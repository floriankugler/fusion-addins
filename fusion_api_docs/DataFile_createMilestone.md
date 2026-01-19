# DataFile.createMilestone Method

Parent Object: [DataFile](DataFile.md)  

## Description

Makes the version this DataFile represents a milestone.

## Syntax

"dataFile_var" is a variable referencing a [DataFile](DataFile.md) object.

```python
returnValue = dataFile_var.createMilestone(milestoneName)
```

## Return Value

| Type | Description |
|----|----|
| [Milestone](Milestone.md) | Returns the created Milestone object or null in the case of failure. One case of failure is if a milestone already exists for this version. |

## Parameters

| Name | Type | Description |
|----|----|----|
| milestoneName | string | The name of the milestone as seen in the data panel and Fusion web client. If an empty string is provided, a default name will be used. |

## Version

Introduced in version March 2024  

