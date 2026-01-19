# Canvas.createForAssemblyContext Method

Parent Object: [Canvas](Canvas.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"canvas_var" is a variable referencing a [Canvas](Canvas.md) object.

```python
returnValue = canvas_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [Canvas](Canvas.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version May 2023  

