# FlatPatternComponent.allOccurrencesByComponent Method

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns all occurrences, at any level of the assembly, that reference the specified component. The returned list is read-only.

## Syntax

"flatPatternComponent_var" is a variable referencing a [FlatPatternComponent](FlatPatternComponent.md) object.

```python
returnValue = flatPatternComponent_var.allOccurrencesByComponent(component)
```

## Return Value

| Type | Description |
|----|----|
| [OccurrenceList](OccurrenceList.md) | The occurrences referenced by the specified component. |

## Parameters

| Name | Type | Description |
|----|----|----|
| component | [Component](Component.md) | The component that is being referenced by the occurrences that will be returned. |

## Version

Introduced in version October 2022  

