# Component.componentColor Property

Parent Object: [Component](Component.md)  

## Description

Gets and sets the color associated with a component. This color is only used when the "Display Component Colors" command is enabled. Enabling the display of component colors is done through the command or API using the Application.isComponentColorsDisplayed property. When this is on, all bodies in a component will display using the color assigned to the component. Fusion randomly assigns a color to a component when it is created. This property allows you to get and change the assigned default color. Setting this property to null results in a new color being randomly assigned by Fusion. This is the equivalent of the "Cycle Component Color" command available in the context menu of a component.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.componentColor

# Set the value of the property.
component_var.componentColor = propertyValue
```

## Property Value

This is a read/write property whose value is a [Color](Color.md).

## Version

Introduced in version May 2024  

