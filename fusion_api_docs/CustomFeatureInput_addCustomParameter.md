# CustomFeatureInput.addCustomParameter Method

Parent Object: [CustomFeatureInput](CustomFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Defines the information needed to create a new custom parameter that will be associated with this feature. A custom parameter appears as a model parameter and will be listed as a child of the custom feature in the parameter dialog. The custom feature will automatically have a dependency on this parameter.

## Syntax

"customFeatureInput_var" is a variable referencing a [CustomFeatureInput](CustomFeatureInput.md) object.

```python
# Uses no optional arguments.
returnValue = customFeatureInput_var.addCustomParameter(id, label, value, units)

# Uses optional arguments.
returnValue = customFeatureInput_var.addCustomParameter(id, label, value, units, isVisible)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the definition of the model parameter was successfully added. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | An id for this parameter. This is used to allow you to identify the parameter in the future. This must be unique with respect to all other parameters associated with this custom feature. It's needed because the label does not need to be unique and the Fusion auto-generated name can be edited by the user. |
| label | string | The label for this parameter as seen in the parameters dialog. This identifies to the user the purpose of this parameter. For example, when you create an extrusion with a specific distance, there are two parameters displayed in the parameters dialog with the labels "AlongDistance" and "TaperAngle". This does not have to be unique because in the case of a fillet feature there can be multiple parameters all labeled "Radius". |
| value | [ValueInput](ValueInput.md) | ValueInput object that specifies the value of the parameter. If the ValueInput was created using a real, the value will be interpreted using the internal unit for the unit type specified by the "units" argument. For example, if the ValueInput was created using the real value 5 and the input to the "units" argument is any valid length unit, the value will be interpreted as 5 centimeters since centimeters is the internal unit for lengths. If the "units" argument is a valid angle unit the value will be interpreted as 5 radians. If the ValueInput was created using a string, the string is used as-is for the expression of the parameter. This means if there are units as part of the string it must evaluate to the same unit type as that specified by the "units" argument and if no units are specified it will use the current default units specified for the current document. For example, if the ValueInput was created with the string "5 in", then the "units" argument must define any valid length so it is compatible. If the ValueInput was created with the string "5", any unit type can be used and the result will be 5 of that unit. When using a ValueInput created using a string, it's the same as creating a parameter in the user-interface. You can specify any valid expression, i.e. "5", "5 in", "5 in / 2", "5 + Length", etc. and you can choose from many different types of units. The only requirement is that the units must match in type. For example, they must both be lengths, or they must both be angles. |
| units | string | The units to use for the value of the parameter. Units specified must match the units specified (if any) in the ValueInput object. To create a parameter with no units (unitless) you can specify either an empty string. |
| isVisible | boolean | Optional argument that specifies if the parameter will be visible in the parameters dialog or not. By default the parameter will be visible. This can be useful in cases where the feature can be edited to be in different states where a parameter is only valid in a certain state. You can change the visibility based on the current state of the feature and if that parameter should be available for edit. This implies that you create all the parameters that might be needed and then change their visibility based on the current state of the feature. The parameters that are not visible will not be returned by the ModelParameters collection and are only available through the custom feature they're associated with. This is an optional argument whose default value is True. |

## Version

Introduced in version January 2021  

