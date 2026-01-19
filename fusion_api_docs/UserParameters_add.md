# UserParameters.add Method

Parent Object: [UserParameters](UserParameters.md)  

## Description

Adds a new user parameter to the collection.

## Syntax

"userParameters_var" is a variable referencing a [UserParameters](UserParameters.md) object.

```python
returnValue = userParameters_var.add(name, value, units, comment)
```

## Return Value

| Type | Description |
|----|----|
| [UserParameter](UserParameter.md) | Returns the newly created UserParameter or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| name | string | The name of the parameter. This is the name shown in the parameters dialog |
| value | [ValueInput](ValueInput.md) | ValueInput object that specifies the value of the parameter. If the ValueInput was created using a real, the value will be interpreted using the internal unit for the unit type specified by the "units" argument. For example, if the ValueInput was created using the real value 5 and the input to the "units" argument is any valid length unit, the value will be interpreted as 5 centimeters since centimeters is the internal unit for lengths. If the "units" argument is a valid angle unit the value will be interpreted as 5 radians. If the ValueInput was created using a string, the string is used as-is for the expression of the parameter. For value parameters, this means if there are units as part of the string, it must evaluate to the same unit type as that specified by the "units" argument and if no units are specified it will use the current default units specified for the current document. For example, if the ValueInput was created with the string "5 in", then the "units" argument must define any valid length so they are compatible. If the ValueInput was created with the string "5", any unit type can be used and the result will be 5 of that unit. If the "units" argument is "Text" then a text parameter will be created using the value provided as the expression. When using a ValueInput created using a string, it's the same as creating a parameter in the user-interface. You can specify any valid expression, i.e. "5", "5 in", "5 in / 2", "5 + Length", etc. and you can choose from many different types of units. The only requirement is that the units must match in type. For example, they must both be lengths, or they must both be angles. When creating a Boolean parameter, you should use the createByBoolean method of the ValueInput object. |
| units | string | The units to use for the value of the parameter. The use of any of the measurement units will result in the creation of a numeric parameter. The units specified must match the units specified (if any) in the ValueInput object. To create a parameter with no units, you can specify an empty string as the units, which will also create a numeric parameter. To create a text parameter, use "Text" as the unit type. |
| comment | string | The comment to display in the parameters dialog. Specify an empty string ("") for no comment |

## Version

Introduced in version August 2014  

