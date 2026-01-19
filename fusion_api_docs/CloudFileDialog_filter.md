# CloudFileDialog.filter Property

Parent Object: [CloudFileDialog](CloudFileDialog.md)  

## Description

Gets or sets the current file type filter. This controls the types of files displayed in the dialog. The filter consists of file extensions separated by a semi-colon. The string below is an example of the filter used by Fusion for the Open command.  

"f3d;f2d;f2t;fbrd;fsch;flbr;fprj;prt;par;sldprt;sldasm;ipt;iam;stp;ste;step"  

An empty string indicates that no filter should be used and all files in the current DataFolder should be displayed.

## Syntax

"cloudFileDialog_var" is a variable referencing a CloudFileDialog object.  

```python
# Get the value of the property.
propertyValue = cloudFileDialog_var.filter

# Set the value of the property.
cloudFileDialog_var.filter = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version October 2022  

