# Occurrence.childOccurrences Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Returns a read only list of child occurrences where only the occurrences in this occurrence's AssemblyContext are returned .

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.childOccurrences
```

## Property Value

This is a read only property whose value is an [OccurrenceList](OccurrenceList.md).

## Samples

| Name | Description |
|----|----|
| [Assembly traversal using recursion API Sample](AssemblyTraversalUsingRecursion_Sample.md) | Traverses the entire structure of the currently open assemlby using a recursive function and displays the result in a message box. This will match the occurrence structure seen in the browser. |

## Version

Introduced in version August 2014  

