# ConfigurationJointSnaps.add Method

Parent Object: [ConfigurationJointSnaps](ConfigurationJointSnaps.md)  

## Description

Adds a new snap to the column. The snaps associated with the column can be used in the cells in the column.

## Syntax

"configurationJointSnaps_var" is a variable referencing a [ConfigurationJointSnaps](ConfigurationJointSnaps.md) object.

```python
returnValue = configurationJointSnaps_var.add(name, jointGeometry)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationJointSnap](ConfigurationJointSnap.md) | Returns the newly created ConfigurationJointSnap. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the new snap. The name must be unique with respect to the other snaps defined for this column. An empty string can be provided, which will cause Fusion to use a default naming scheme to create a name. |
| jointGeometry | [Base](Base.md) | A JointGeometry object that defines how the snap is defined. When creating the JointGeometry object, it must be limited to geometry in the occurrence associated with the column. |

## Version

Introduced in version September 2024  

