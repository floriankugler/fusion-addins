# ControllerConfigurationMachineElement.tcpRapidInterpolationMode Property

Parent Object: [ControllerConfigurationMachineElement](ControllerConfigurationMachineElement.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Specifies how the CNC machine axes behave during rapid moves when TCP (Tool Center Point) is active, as defined in the machine's controller. Independent Axes moves the axes independently at maximum speed, potentially resulting in different completion times for each axis. Synchronized Axes moves the axes together, completing the motion simultaneously, although the tool's tip may deviate from the direct line between the start and finish points. Tool Tip adjusts the linear axes to keep the tool's tip positioned along the direct line between the start and finish points.

## Syntax

"controllerConfigurationMachineElement_var" is a variable referencing a ControllerConfigurationMachineElement object.  

```python
# Get the value of the property.
propertyValue = controllerConfigurationMachineElement_var.tcpRapidInterpolationMode

# Set the value of the property.
controllerConfigurationMachineElement_var.tcpRapidInterpolationMode = propertyValue
```

## Property Value

This is a read/write property whose value is a [MachineTCPInterpolationMode](MachineTCPInterpolationMode.md).

## Version

Introduced in version September 2025  

