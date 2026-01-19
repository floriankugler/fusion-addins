# Script.run Method

Parent Object: [Script](Script.md)  

## Description

Runs this script or add-in, if it's not already running.

## Syntax

"script_var" is a variable referencing a [Script](Script.md) object.

```python
# Uses no optional arguments.
returnValue = script_var.run()

# Uses optional arguments.
returnValue = script_var.run(waitForFinish)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| waitForFinish | boolean | Specifies if call will wait until the script or add-in has finished running. For add-ins, this should always be false, because they typically continue to run for the entire Fusion session. For scripts, there are cases where you might want to set this to true, where you need to wait for the script to finish because you want to do something with whatever it creates. Typically, this should be false, so it starts the script and immediately returns. This is an optional argument whose default value is False. |

## Version

Introduced in version October 2023  

