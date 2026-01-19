# Occurrences.addNewComponent Method

Parent Object: [Occurrences](Occurrences.md)  

## Description

Method that creates a new component and an occurrence that references it.

## Syntax

"occurrences_var" is a variable referencing an [Occurrences](Occurrences.md) object.

```python
returnValue = occurrences_var.addNewComponent(transform)
```

## Return Value

| Type | Description |
|----|----|
| [Occurrence](Occurrence.md) | Returns the newly created occurrence or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| transform | [Matrix3D](Matrix3D.md) | A transform that defines the location for the new occurrence. |

## Samples

| Name | Description |
|----|----|
| [Component Sample](ComponentSample_Sample.md) | Component related functions |

## Version

Introduced in version August 2014  

