# Occurrence.deleteMe Method

Parent Object: [Occurrence](Occurrence.md)  

## Description

Deletes the occurrence from the design. If this is the last occurrence referencing a specific Component, the component is also deleted.

## Syntax

"occurrence_var" is a variable referencing an [Occurrence](Occurrence.md) object.

```python
returnValue = occurrence_var.deleteMe()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Samples

| Name | Description |
|----|----|
| [Delete Empty Components](DeleteEmptyComponents_Sample.md) | Deletes empty components from the active design. |

## Version

Introduced in version August 2014  

