# Command.helpFile Property

Parent Object: [Command](Command.md)  

## Description

Gets and sets the associated HTML help file for this command.

## Remarks

If this is defined then the help button will be displayed in the lower-left corner of the command dialog and when clicked the help file will be displayed using the application defined by the operating system for that file type.For example, if the helpFile property references a .htm or .html file, the default browser will be invoked to display the file. If a .pdf file is used then whatever the default application is for viewing a PDF file will be invoked.

The file referenced must be a local file and cannot be a URL. However, you can use a local HTML file that redirects to a URL.

```python
<html>
  <head>
     <meta http-equiv="refresh" content="0; url=http://example.com/" />
  </head>
  <body></body>
</html>
```

The filename can be either a full path or a relative path with respect to the script or add-in .py, .js, .dll, or .dylib file. If this is an empty string, (which is the default), then the help button will not be displayed.

## Syntax

"command_var" is a variable referencing a Command object.  

```python
# Get the value of the property.
propertyValue = command_var.helpFile

# Set the value of the property.
command_var.helpFile = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version May 2016  

