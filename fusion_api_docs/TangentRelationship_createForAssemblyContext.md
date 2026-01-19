# TangentRelationship.createForAssemblyContext Method

Parent Object: [TangentRelationship](TangentRelationship.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"tangentRelationship_var" is a variable referencing a [TangentRelationship](TangentRelationship.md) object.

```python
returnValue = tangentRelationship_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [TangentRelationship](TangentRelationship.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version May 2022  

