# RigidGroup.setOccurrences Method

Parent Object: [RigidGroup](RigidGroup.md)  

## Description

Sets which occurrences are to be part of this rigid group.  

To use this method, you need to position the timeline marker to immediately before this group. This can be accomplished using the following code: group.timelineObject.rollTo(True)

## Syntax

"rigidGroup_var" is a variable referencing a [RigidGroup](RigidGroup.md) object.

```python
returnValue = rigidGroup_var.setOccurrences(occurrences, includeChildren)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrences | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the occurrences to use in creating the rigid group. |
| includeChildren | boolean | Boolean indicating if the children of the input occurrences should be included in the rigid group. |

## Version

Introduced in version September 2015  

