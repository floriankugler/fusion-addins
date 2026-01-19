# FloatSliderCommandInput.setText Method

Parent Object: [FloatSliderCommandInput](FloatSliderCommandInput.md)  

## Description

Sets the text of the slider. Both the left and the right text should be set.

## Syntax

"floatSliderCommandInput_var" is a variable referencing a [FloatSliderCommandInput](FloatSliderCommandInput.md) object.

```python
returnValue = floatSliderCommandInput_var.setText(left, right)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name  | Type   | Description                                         |
|-------|--------|-----------------------------------------------------|
| left  | string | Indicates the text on the left side of the slider.  |
| right | string | Indicates the text on the right side of the slider. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version June 2015  

