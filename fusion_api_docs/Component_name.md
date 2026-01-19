# Component.name Property

Parent Object: [Component](Component.md)  

## Description

Property that gets and sets the name of this component. This is the name shown in the browser for each occurrence referencing this component.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.name

# Set the value of the property.
component_var.name = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Samples

| Name | Description |
| --- | --- |
| [Delete Empty Components](DeleteEmptyComponents_Sample.md) | Deletes empty components from the active design. |
| [Set Vise Origin As Setup WCS Origin API Sample](SetViseOriginAsSetupWCSOrigin_Sample.md) | This sample script demonstrates how to define our setup WCS origin relative to our vise origin from either a component, a sketch point or a joint origin. The Work Coordinate System is a reference point set in our CAM workspace and on our machine. All machine coordinates are drawn from the WCS. This script demonstrates defining the WCS by each of 4 alternative methods: Setup by default with no origin defined. Setup using vise origin as WCS origin. Setup using a sketch point as WCS origin. Setup using a joint origin as WCS origin. |

## Version

Introduced in version August 2014  

