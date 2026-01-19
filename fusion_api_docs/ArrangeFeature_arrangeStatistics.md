# ArrangeFeature.arrangeStatistics Property

Parent Object: [ArrangeFeature](ArrangeFeature.md)  

## Description

Returns statistics about the arrangement in JSON format as a string. Each item in the JSON is identified with its English name, and the current localized name is also provided. The values follow the API rules, where all length values are in centimeters, and areas are in square centimeters. The returned JSON may include additional values in the future, so code consuming this output should be tolerant of new fields.  

Returns an empty string in the case it failed to get any statistics.

## Syntax

"arrangeFeature_var" is a variable referencing an ArrangeFeature object.  

```python
# Get the value of the property.
propertyValue = arrangeFeature_var.arrangeStatistics
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version July 2025  

