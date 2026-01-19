# PathEntity.createForAssemblyContext Method

Parent Object: [PathEntity](PathEntity.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"pathEntity_var" is a variable referencing a [PathEntity](PathEntity.md) object.

```python
returnValue = pathEntity_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [PathEntity](PathEntity.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name       | Type                         | Description |
|------------|------------------------------|-------------|
| occurrence | [Occurrence](Occurrence.md) |             |

## Version

Introduced in version November 2014  

