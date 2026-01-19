# RecognizedHolesInput.filterPartialHoles Property

Parent Object: [RecognizedHolesInput](RecognizedHolesInput.md)  

## Description

Partial holes will not be included in recognized holes when set to true. Holes that intersect edges are considered partial holes. If a hole has multiple segments, such as a counterbore hole, all the segments inside the hole must intersect an edge for the hole to be considered a partial hole.

## Syntax

"recognizedHolesInput_var" is a variable referencing a RecognizedHolesInput object.  

```python
# Get the value of the property.
propertyValue = recognizedHolesInput_var.filterPartialHoles

# Set the value of the property.
recognizedHolesInput_var.filterPartialHoles = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2024  

