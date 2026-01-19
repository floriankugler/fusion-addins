# MultiAxisRetractAndReconfigureSettings.safePlungeFeedrate Property

Parent Object: [MultiAxisRetractAndReconfigureSettings](MultiAxisRetractAndReconfigureSettings.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The safe plunge feedrate for plunge moves. A plunge rate is the speed at which the tool is driven down into the material when starting a cut. It varies depending on the tool and material. Plunging too fast may damage the tip of the cutter. (cm/min)

## Syntax

"multiAxisRetractAndReconfigureSettings_var" is a variable referencing a MultiAxisRetractAndReconfigureSettings object.  

```python
# Get the value of the property.
propertyValue = multiAxisRetractAndReconfigureSettings_var.safePlungeFeedrate

# Set the value of the property.
multiAxisRetractAndReconfigureSettings_var.safePlungeFeedrate = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version September 2025  

