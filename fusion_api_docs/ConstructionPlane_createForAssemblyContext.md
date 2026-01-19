# ConstructionPlane.createForAssemblyContext Method

Parent Object: [ConstructionPlane](ConstructionPlane.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"constructionPlane_var" is a variable referencing a [ConstructionPlane](ConstructionPlane.md) object.

```python
returnValue = constructionPlane_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ConstructionPlane](ConstructionPlane.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

