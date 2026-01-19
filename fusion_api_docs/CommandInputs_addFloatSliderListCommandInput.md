# CommandInputs.addFloatSliderListCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new slider input to the command. The value type is float.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
# Uses no optional arguments.
returnValue = commandInputs_var.addFloatSliderListCommandInput(id, name, unitType, valueList)

# Uses optional arguments.
returnValue = commandInputs_var.addFloatSliderListCommandInput(id, name, unitType, valueList, hasTwoSliders)
```

## Return Value

| Type | Description |
|----|----|
| [FloatSliderCommandInput](FloatSliderCommandInput.md) | Returns the created FloatSliderCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed name of this command as seen in the dialog. |
| unitType | string | The unit type of the value. This will be used to validate the input and the returned Value object will be of this type. |
| valueList | double[] | Provides the value list (in database units) of the slider command input. This defines all of the values that the slider can return. As the user moves the slider it will jump between these values. The low and high values of the list are used as the minimum and maximum values of the slider. |
| hasTwoSliders | boolean | Optional input. Indicates if the slider input has two sliders. This is an optional argument whose default value is False. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version June 2015  

