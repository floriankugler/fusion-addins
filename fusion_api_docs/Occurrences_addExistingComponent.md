# Occurrences.addExistingComponent Method

Parent Object: [Occurrences](Occurrences.md)  

## Description

Method that creates a new occurrence using an existing component. This is the equivalent of copying and pasting an occurrence in the user interface.

## Syntax

"occurrences_var" is a variable referencing an [Occurrences](Occurrences.md) object.

```python
returnValue = occurrences_var.addExistingComponent(component, transform)
```

## Return Value

| Type | Description |
|----|----|
| [Occurrence](Occurrence.md) | Returns the newly created occurrence or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| component | [Component](Component.md) | The existing component to create a new occurrence of. |
| transform | [Matrix3D](Matrix3D.md) | A transform that defines the location for the new occurrence |

## Samples

| Name | Description |
|----|----|
| [Component Sample](ComponentSample_Sample.md) | Component related functions |

## Version

Introduced in version August 2014  

