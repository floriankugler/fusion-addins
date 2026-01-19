# Path.createForAssemblyContext Method

Parent Object: [Path](Path.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"path_var" is a variable referencing a [Path](Path.md) object.

```python
returnValue = path_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [Path](Path.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name       | Type                         | Description |
|------------|------------------------------|-------------|
| occurrence | [Occurrence](Occurrence.md) |             |

## Version

Introduced in version November 2014  

