# Occurrence.isIsolated Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Gets and sets whether this occurrence is isolated in the UI. When an occurrence is isolated it is the only one visible in the user-interface. Only one occurrence can be isolated at a time so setting this property to true will un-isolate an occurrence that is currently isolated. Setting this property to false for an occurrence that is current isolated will un-isolate it so that no occurrence will be isolated.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.isIsolated

# Set the value of the property.
occurrence_var.isIsolated = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version June 2015  

