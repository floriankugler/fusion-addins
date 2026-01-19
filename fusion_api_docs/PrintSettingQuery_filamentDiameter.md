# PrintSettingQuery.filamentDiameter Property

Parent Object: [PrintSettingQuery](PrintSettingQuery.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

The filament diameter specifies filament diameter for FFF Printer. This should match the FFF PrintSetting filament diameter in cm.

## Remarks

This property has been retired. The machine now contains the filament diameter(s) in the extruder(s).

## Syntax

"printSettingQuery_var" is a variable referencing a PrintSettingQuery object.  

```python
# Get the value of the property.
propertyValue = printSettingQuery_var.filamentDiameter

# Set the value of the property.
printSettingQuery_var.filamentDiameter = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version April 2023  
Retired in version July 2023  

