# ArrangeFeatureInput.set3DEnvelope Method

Parent Object: [ArrangeFeatureInput](ArrangeFeatureInput.md)  

## Description

Defines a 3D envelope input. Only a single envelope input can exist at time. Calling this method will cause any existing envelope input object to be invalid.

## Syntax

"arrangeFeatureInput_var" is a variable referencing an [ArrangeFeatureInput](ArrangeFeatureInput.md) object.

```python
returnValue = arrangeFeatureInput_var.set3DEnvelope(plane, length, width, height)
```

## Return Value

| Type | Description |
|----|----|
| [Arrange3DEnvelopeInput](Arrange3DEnvelopeInput.md) | Returns the created Arrange3DEnvelopeInput object or null if the creation fails. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| plane | [ConstructionPlane](ConstructionPlane.md) | The Construction plane the envelope will be on. |
| length | [ValueInput](ValueInput.md) | The length of the envelope. This is the size of the envelope as measured along the X axis of the specified construction plane. This value will become a parameter when the arrangement is created. If the ValueInput is created using a real number it is in centimeters. If you use a string, it is evaluated the same as a value would be in the command dialog and uses the current document units. For example, if the document units are inch and you specific "0.25" it will result in 1/4 inch clearance. Using a string, you can also specify the units as part of the expression, such as "0.25 in + 2 mm". And you can define equations like "PartSize + 2 mm" where "PartSize" is an existing parameter. |
| width | [ValueInput](ValueInput.md) | The width of the envelope. This is the size of the envelope as measured along the Y axis of the specified construction plane. This value will become a parameter when the arrangement is created. If the ValueInput is created using a real number it is in centimeters. If you use a string, it is evaluated the same as a value would be in the command dialog and uses the current document units. For example, if the document units are inch and you specific "0.25" it will result in 1/4 inch clearance. Using a string, you can also specify the units as part of the expression, such as "0.25 in + 2 mm". And you can define equations like "PartSize + 2 mm" where "PartSize" is an existing parameter. |
| height | [ValueInput](ValueInput.md) | The height of the envelope. This is the size of the envelope as measured along the Z axis of the specified construction plane. This value will become a parameter when the arrangement is created. If the ValueInput is created using a real number it is in centimeters. If you use a string, it is evaluated the same as a value would be in the command dialog and uses the current document units. For example, if the document units are inch and you specific "0.25" it will result in 1/4 inch clearance. Using a string, you can also specify the units as part of the expression, such as "0.25 in + 2 mm". And you can define equations like "PartSize + 2 mm" where "PartSize" is an existing parameter. |

## Version

Introduced in version January 2025  

