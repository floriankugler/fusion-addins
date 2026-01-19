# SetupInput.fixtureEnabled Property

Parent Object: [SetupInput](SetupInput.md)  

## Description

Set this value to enable the use of fixtures for this setup. To then set the fixture models themselves use the \`fixtures\` property.

## Syntax

"setupInput_var" is a variable referencing a SetupInput object.  

```python
# Get the value of the property.
propertyValue = setupInput_var.fixtureEnabled

# Set the value of the property.
setupInput_var.fixtureEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
| --- | --- |
| [Set Vise Origin As Setup WCS Origin API Sample](SetViseOriginAsSetupWCSOrigin_Sample.md) | This sample script demonstrates how to define our setup WCS origin relative to our vise origin from either a component, a sketch point or a joint origin. The Work Coordinate System is a reference point set in our CAM workspace and on our machine. All machine coordinates are drawn from the WCS. This script demonstrates defining the WCS by each of 4 alternative methods: Setup by default with no origin defined. Setup using vise origin as WCS origin. Setup using a sketch point as WCS origin. Setup using a joint origin as WCS origin. |

## Version

Introduced in version April 2023  

