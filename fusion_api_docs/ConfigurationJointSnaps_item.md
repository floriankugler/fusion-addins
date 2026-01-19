# ConfigurationJointSnaps.item Method

Parent Object: [ConfigurationJointSnaps](ConfigurationJointSnaps.md)  

## Description

A method that returns the specified snap using an index into the collection.

## Syntax

"configurationJointSnaps_var" is a variable referencing a [ConfigurationJointSnaps](ConfigurationJointSnaps.md) object.

```python
returnValue = configurationJointSnaps_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationJointSnap](ConfigurationJointSnap.md) | Returns the specified snap or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the snap to return, where the first row is index 0. |

## Version

Introduced in version September 2024  

