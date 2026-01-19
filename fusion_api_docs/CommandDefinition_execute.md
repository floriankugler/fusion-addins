# CommandDefinition.execute Method

Parent Object: [CommandDefinition](CommandDefinition.md)  

## Description

Executes this command definition. This is the same as the user clicking a button that is associated with this command definition.

## Remarks

The execute method is not supported within any of the Command related events because it results in starting a new command which has the side-effect of terminating the current command, which is your running command.

## Syntax

"commandDefinition_var" is a variable referencing a [CommandDefinition](CommandDefinition.md) object.

```python
# Uses no optional arguments.
returnValue = commandDefinition_var.execute()

# Uses optional arguments.
returnValue = commandDefinition_var.execute(input)
```

## Return Value

| Type    | Description                                                       |
|---------|-------------------------------------------------------------------|
| boolean | Returns true or false indicating if the execution was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| input | [NamedValues](NamedValues.md) | This argument is ignored and exists for possible future use. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |
| [Custom Event Sample](CustomEventSample_Sample.md) | Demonstrates the ability to call into the main thread from a worker thread. This sample is an add-in. To use it, use the Scripts and Add-Ins command to create a new add-in. Delete all of the code in the newly created add-in and replace it with the code below. Have a model open that has a parameter named "Length". Load the add-in. The add-in will change the value of the parameter every two seconds using a random value between 1 and 10. |

## Version

Introduced in version August 2014  

