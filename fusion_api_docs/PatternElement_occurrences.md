# PatternElement.occurrences Property

Parent Object: [PatternElement](PatternElement.md)  

## Description

If the patternEntityType property of the parent feature returns OccurrencesPatternType then this property will return the occurrences associated with this particular pattern element.

## Syntax

"patternElement_var" is a variable referencing a PatternElement object.  

```python
# Get the value of the property.
propertyValue = patternElement_var.occurrences
```

## Property Value

This is a read only property whose value is an array of type [Occurrence](Occurrence.md).

## Version

Introduced in version July 2015  

