# SMTExportOptions.version Property

Parent Object: [SMTExportOptions](SMTExportOptions.md)  

## Description

Gets and set the version of the SMT format to write to. The default is to use the current version of the Autodesk Shape Manager kernel that Fusion is using. Specifying an invalid version will result in an assert.  

Valid versions are 218 up to the current version, which is what this property returns by default when a new SMTExportOptions object is created.

## Syntax

"sMTExportOptions_var" is a variable referencing a SMTExportOptions object.  

```python
# Get the value of the property.
propertyValue = sMTExportOptions_var.version

# Set the value of the property.
sMTExportOptions_var.version = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version April 2019  

