# ShellFeature.createForAssemblyContext Method

Parent Object: [ShellFeature](ShellFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"shellFeature_var" is a variable referencing a [ShellFeature](ShellFeature.md) object.

```python
returnValue = shellFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ShellFeature](ShellFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version November 2014  

