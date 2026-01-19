# TimelineGroup.deleteMe Method

Parent Object: [TimelineGroup](TimelineGroup.md)  

## Description

Deletes the group with the option of deleting or keeping the contents.

## Syntax

"timelineGroup_var" is a variable referencing a [TimelineGroup](TimelineGroup.md) object.

```python
returnValue = timelineGroup_var.deleteMe(deleteGroupAndContents)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| deleteGroupAndContents | boolean | Indicates if the group and its contents should be deleted or if only the group should be deleted and the contents kept and expanded. A value of true will delete the group and its contents. |

## Version

Introduced in version August 2014  

