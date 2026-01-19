# Component.occurrences Property

Parent Object: [Component](Component.md)  

## Description

Property that returns the Occurrences collection associated with this component. This provides access to the occurrences at the top-level of this component and provides the functionality to add new occurrences.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.occurrences
```

## Property Value

This is a read only property whose value is an [Occurrences](Occurrences.md).

## Samples

| Name | Description |
|----|----|
| [Assembly traversal using recursion API Sample](AssemblyTraversalUsingRecursion_Sample.md) | Traverses the entire structure of the currently open assemlby using a recursive function and displays the result in a message box. This will match the occurrence structure seen in the browser. |

## Version

Introduced in version August 2014  

