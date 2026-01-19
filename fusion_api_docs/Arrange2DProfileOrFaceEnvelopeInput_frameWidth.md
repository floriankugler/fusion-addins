# Arrange2DProfileOrFaceEnvelopeInput.frameWidth Property

Parent Object: [Arrange2DProfileOrFaceEnvelopeInput](Arrange2DProfileOrFaceEnvelopeInput.md)  

## Description

Specifies the minimum distance between the components in the arrangement and the envelope frame.  

This value will become a parameter when the arrangement is created. If the ValueInput is created using a real number it is in centimeters. If you use a string, it is evaluated the same as a value would be in the command dialog and uses the current document units. For example, if the document units are inch and you specific "0.25" it will result in 1/4 inch clearance. You can also specify the units as part of the expression, such as "0.25 in + 2 mm". And you can define equations like "ToolDia + 2 mm" where "ToolDia" is an existing parameter.

## Syntax

"arrange2DProfileOrFaceEnvelopeInput_var" is a variable referencing an Arrange2DProfileOrFaceEnvelopeInput object.  

```python
# Get the value of the property.
propertyValue = arrange2DProfileOrFaceEnvelopeInput_var.frameWidth

# Set the value of the property.
arrange2DProfileOrFaceEnvelopeInput_var.frameWidth = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version January 2025  

