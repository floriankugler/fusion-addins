# StockMaterial.hardness Property

Parent Object: [StockMaterial](StockMaterial.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Get and sets the hardness of the stock materials. NOTE: the hardness can be NaN if not set. and user can set the hardness to NaN.

## Syntax

"stockMaterial_var" is a variable referencing a StockMaterial object.  

```python
# Get the value of the property.
propertyValue = stockMaterial_var.hardness

# Set the value of the property.
stockMaterial_var.hardness = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version November 2024  

