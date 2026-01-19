# MachineParts.add Method

Parent Object: [MachineParts](MachineParts.md)  

## Description

Add a new part to this collection. The part's parent will be set to the owner of this collection, or null if this is the root parts collection.  

If the passed MachinePartInput has a MachineAxisInput a new MachineAxis will be created.

## Syntax

"machineParts_var" is a variable referencing a [MachineParts](MachineParts.md) object.

```python
returnValue = machineParts_var.add(partInput)
```

## Return Value

| Type | Description |
|----|----|
| [MachinePart](MachinePart.md) | Returns the newly created MachinePart or null if creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| partInput | [MachinePartInput](MachinePartInput.md) | Part input object used to create the new MachinePart. |

## Version

Introduced in version April 2023  

