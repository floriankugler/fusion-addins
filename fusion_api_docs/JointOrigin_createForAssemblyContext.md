# JointOrigin.createForAssemblyContext Method

Parent Object: [JointOrigin](JointOrigin.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"jointOrigin_var" is a variable referencing a [JointOrigin](JointOrigin.md) object.

```python
returnValue = jointOrigin_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [JointOrigin](JointOrigin.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version September 2015  

