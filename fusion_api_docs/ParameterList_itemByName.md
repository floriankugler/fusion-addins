# ParameterList.itemByName Method

Parent Object: [ParameterList](ParameterList.md)  

## Description

Returns the specified parameter using the name of the parameter as it is displayed in the parameters dialog

## Syntax

"parameterList_var" is a variable referencing a [ParameterList](ParameterList.md) object.

```python
returnValue = parameterList_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Parameter](Parameter.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the parameter as it is displayed in the parameters dialog |

## Samples

| Name | Description |
|----|----|
| [Create Animation API Sample](CreateAnimation_Sample.md) | Creates a series of images of a design where a parameter is being changed. The series of images can be used to create an animation using other software. To run this sample, have a part open that contains a parameter named "Length". The parameter should be able to be successfully modified from 10 to 15 centimeters. Run the sample and choose or create a directory for the output. After running you should have a folder full of images that are snapshots of each parameter value. |

## Version

Introduced in version August 2014  

