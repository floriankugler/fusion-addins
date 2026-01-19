# Application.supportedProductTypes Property

Parent Object: [Application](Application.md)  

## Description

Returns an array containing the names of the products types currently supported by Fusion. For example, the name returned for Fusion is "DesignProductType". These product type names are used to identify specific products in some other API functions such as the productType property on the Workspace and ToolbarPanel objects.

## Syntax

"application_var" is a variable referencing an Application object.  

```python
# Get the value of the property.
propertyValue = application_var.supportedProductTypes
```

## Property Value

This is a read only property whose value is an array of type string.

## Version

Introduced in version June 2015  

