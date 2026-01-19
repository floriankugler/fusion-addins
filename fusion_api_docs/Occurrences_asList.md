# Occurrences.asList Property

Parent Object: [Occurrences](Occurrences.md)  

## Description

Returns the contents of this collection as an OccurrencesList object. This is useful when writing a function that traverses an assembly.

## Syntax

"occurrences_var" is a variable referencing an Occurrences object.  

```python
# Get the value of the property.
propertyValue = occurrences_var.asList
```

## Property Value

This is a read only property whose value is an [OccurrenceList](OccurrenceList.md).

## Samples

| Name | Description |
|----|----|
| [Assembly traversal using recursion API Sample](AssemblyTraversalUsingRecursion_Sample.md) | Traverses the entire structure of the currently open assemlby using a recursive function and displays the result in a message box. This will match the occurrence structure seen in the browser. |

## Version

Introduced in version August 2014  

