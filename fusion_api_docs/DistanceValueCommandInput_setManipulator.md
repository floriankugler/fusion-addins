# DistanceValueCommandInput.setManipulator Method

Parent Object: [DistanceValueCommandInput](DistanceValueCommandInput.md)  

## Description

Defines the position and orientation of the manipulator. The manipulator is only visible when both the isVisible and isEnabled properties are true. If those properties are true and the setManipulator has not been called, the manipulator will be displayed in a default location (0,0,0) and direction (1,0,0). Because of that the input is typically set to be invisible and/or disabled and then enabled once enough input has been specified that you can display the manipulator in the desired location.

## Syntax

"distanceValueCommandInput_var" is a variable referencing a [DistanceValueCommandInput](DistanceValueCommandInput.md) object.

```python
returnValue = distanceValueCommandInput_var.setManipulator(origin, direction)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | Defines the position of the manipulator in root component space. |
| direction | [Vector3D](Vector3D.md) | Defines the direction of the manipulator in root component space. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2016  

