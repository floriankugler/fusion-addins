# RigidGroup.createForAssemblyContext Method

Parent Object: [RigidGroup](RigidGroup.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"rigidGroup_var" is a variable referencing a [RigidGroup](RigidGroup.md) object.

```python
returnValue = rigidGroup_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [RigidGroup](RigidGroup.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version January 2016  

