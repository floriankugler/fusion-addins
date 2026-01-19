# Occurrence.fullPathName Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

The name of the occurrence, including the full path of occurrences as seen in the browser. The top-level component will depend on the context but will typically be the root component of the design. A name for an occurrence that is at the third level of an assembly could be "Sub1:1+Sub2:1+PartA:1".

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.fullPathName
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version August 2014  

