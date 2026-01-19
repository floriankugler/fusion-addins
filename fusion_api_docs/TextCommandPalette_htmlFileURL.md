# TextCommandPalette.htmlFileURL Property

Parent Object: [TextCommandPalette](TextCommandPalette.md)  

## Description

Gets and sets the URL to the HTML file that will be displayed in the palette. This can be a local file or a URL on the web where the HTML will be read. To avoid reading a file, this can also be the full HTML definition as a string.  

If you are providing the HTML content as a string, it should begin with the

element. Any references made in the HTML should be to URL's and not local files since the local path is ambiguous.

## Syntax

"textCommandPalette_var" is a variable referencing a TextCommandPalette object.  

```python
# Get the value of the property.
propertyValue = textCommandPalette_var.htmlFileURL

# Set the value of the property.
textCommandPalette_var.htmlFileURL = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version August 2017  

