# ProfileCurve.createForAssemblyContext Method

Parent Object: [ProfileCurve](ProfileCurve.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. Returns null if this isn't the NativeObject.

## Syntax

"profileCurve_var" is a variable referencing a [ProfileCurve](ProfileCurve.md) object.

```python
returnValue = profileCurve_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ProfileCurve](ProfileCurve.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

