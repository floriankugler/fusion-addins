# ConfigurationJointSnaps.itemByName Method

Parent Object: [ConfigurationJointSnaps](ConfigurationJointSnaps.md)  

## Description

A method that returns the snap with the specified name.

## Syntax

"configurationJointSnaps_var" is a variable referencing a [ConfigurationJointSnaps](ConfigurationJointSnaps.md) object.

```python
returnValue = configurationJointSnaps_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationJointSnap](ConfigurationJointSnap.md) | Returns the specified snap or null if a snap with the specified name does not exist. |

## Parameters

| Name | Type   | Description                     |
|------|--------|---------------------------------|
| name | string | The name of the snap to return. |

## Version

Introduced in version September 2024  

