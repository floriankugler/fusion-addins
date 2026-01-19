# Snapshots.revertPendingSnapshot Method

Parent Object: [Snapshots](Snapshots.md)  

## Description

Reverts and changes that have been made that can be snapshot. This effectively reverts the design back to the last snapshot. This is only valid when the HasPendingSnapshot property returns true.

## Syntax

"snapshots_var" is a variable referencing a [Snapshots](Snapshots.md) object.

```python
returnValue = snapshots_var.revertPendingSnapshot()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the revert was successful. |

## Version

Introduced in version August 2014  

