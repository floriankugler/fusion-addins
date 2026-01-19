# RigidGroups.add Method

Parent Object: [RigidGroups](RigidGroups.md)  

## Description

Creates a new rigid group.

## Syntax

"rigidGroups_var" is a variable referencing a [RigidGroups](RigidGroups.md) object.

```python
returnValue = rigidGroups_var.add(occurrences, includeChildren)
```

## Return Value

| Type | Description |
|----|----|
| [RigidGroup](RigidGroup.md) | Returns the new RigidGroup object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrences | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the occurrences to use in creating the rigid group. |
| includeChildren | boolean | Boolean indicating if the children of the input occurrences should be included in the rigid group. |

## Samples

| Name | Description |
|----|----|
| [Rigid Group API Sample](RigidGroupSample_Sample.md) | Demonstrates creating a new Rigid Group. |

## Version

Introduced in version September 2015  

