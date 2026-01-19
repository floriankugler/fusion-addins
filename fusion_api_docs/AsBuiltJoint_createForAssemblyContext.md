# AsBuiltJoint.createForAssemblyContext Method

Parent Object: [AsBuiltJoint](AsBuiltJoint.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"asBuiltJoint_var" is a variable referencing an [AsBuiltJoint](AsBuiltJoint.md) object.

```python
returnValue = asBuiltJoint_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [AsBuiltJoint](AsBuiltJoint.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version September 2015  

