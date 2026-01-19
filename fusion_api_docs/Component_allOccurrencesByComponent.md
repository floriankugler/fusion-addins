# Component.allOccurrencesByComponent Method

Parent Object: [Component](Component.md)  

## Description

Returns all occurrences, at any level of the assembly, that reference the specified component. The returned list is read-only.

## Syntax

"component_var" is a variable referencing a [Component](Component.md) object.

```python
returnValue = component_var.allOccurrencesByComponent(component)
```

## Return Value

| Type | Description |
|----|----|
| [OccurrenceList](OccurrenceList.md) | The occurrences referenced by the specified component. |

## Parameters

| Name | Type | Description |
|----|----|----|
| component | [Component](Component.md) | The component that is being referenced by the occurrences that will be returned. |

## Samples

| Name | Description |
|----|----|
| [Delete Empty Components](DeleteEmptyComponents_Sample.md) | Deletes empty components from the active design. |

## Version

Introduced in version August 2014  

