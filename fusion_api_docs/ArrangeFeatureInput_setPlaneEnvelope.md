# ArrangeFeatureInput.setPlaneEnvelope Method

Parent Object: [ArrangeFeatureInput](ArrangeFeatureInput.md)  

## Description

Defines an envelope input defined by a plane for the arrange feature. Only a single envelope input can exist at a time. Calling this method will cause any existing envelope object input that has been created for this input to be invalid.

## Syntax

"arrangeFeatureInput_var" is a variable referencing an [ArrangeFeatureInput](ArrangeFeatureInput.md) object.

```python
returnValue = arrangeFeatureInput_var.setPlaneEnvelope(plane, length, width)
```

## Return Value

| Type | Description |
|----|----|
| [Arrange2DPlaneEnvelopeInput](Arrange2DPlaneEnvelopeInput.md) | Returns the created Arrange2DPlaneEnvelopeInput object or null if the creation fails. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| plane | [ConstructionPlane](ConstructionPlane.md) | The Construction plane the envelope will be on. |
| length | [ValueInput](ValueInput.md) | The length of the envelope. This is the size of the envelope as measured along the X axis of the specified construction plane. This value will become a parameter when the arrangement is created. If the ValueInput is created using a real number it is in centimeters. If you use a string, it is evaluated the same as a value would be in the command dialog and uses the current document units. For example, if the document units are inch and you specific "0.25" it will result in 1/4 inch clearance. Using a string, you can also specify the units as part of the expression, such as "0.25 in + 2 mm". And you can define equations like "PartSize + 2 mm" where "PartSize" is an existing parameter. |
| width | [ValueInput](ValueInput.md) | The width of the envelope. This is the size of the envelope as measured along the Y axis of the specified construction plane. This value will become a parameter when the arrangement is created. If the ValueInput is created using a real number it is in centimeters. If you use a string, it is evaluated the same as a value would be in the command dialog and uses the current document units. For example, if the document units are inch and you specific "0.25" it will result in 1/4 inch clearance. Using a string, you can also specify the units as part of the expression, such as "0.25 in + 2 mm". And you can define equations like "PartSize + 2 mm" where "PartSize" is an existing parameter. |

## Version

Introduced in version January 2025  

