# Component.occurrencesByComponent Method

Parent Object: [Component](Component.md)  

## Description

Returns all occurrences at the top-level of this component that reference the specified component. The returned list is read-only.

## Syntax

"component_var" is a variable referencing a [Component](Component.md) object.

```python
returnValue = component_var.occurrencesByComponent(component)
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

Introduced in version August 2014  

