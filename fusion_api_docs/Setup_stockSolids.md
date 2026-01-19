# Setup.stockSolids Property

Parent Object: [Setup](Setup.md)  

## Description

Gets and sets the stock solids associated with the setup, which are represented by an ObjectCollection of models, where a model can be an Occurrence, BRepBody, or MeshBody. StockMode has to be set to \`SolidStock\` otherwise this will throw an error.

## Syntax

"setup_var" is a variable referencing a Setup object.  

```python
# Get the value of the property.
propertyValue = setup_var.stockSolids

# Set the value of the property.
setup_var.stockSolids = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Samples

| Name | Description |
| --- | --- |
| [Set Vise Origin As Setup WCS Origin API Sample](SetViseOriginAsSetupWCSOrigin_Sample.md) | This sample script demonstrates how to define our setup WCS origin relative to our vise origin from either a component, a sketch point or a joint origin. The Work Coordinate System is a reference point set in our CAM workspace and on our machine. All machine coordinates are drawn from the WCS. This script demonstrates defining the WCS by each of 4 alternative methods: Setup by default with no origin defined. Setup using vise origin as WCS origin. Setup using a sketch point as WCS origin. Setup using a joint origin as WCS origin. |

## Version

Introduced in version August 2020  

