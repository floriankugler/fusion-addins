# Palette.htmlFileURL Property

Parent Object: [Palette](Palette.md)  

## Description

Gets and sets the URL to the HTML file that will be displayed in the palette. This can be a local file or a URL on the web where the HTML will be read. To avoid reading a file, this can also be the full HTML definition as a string.  

If you are providing the HTML content as a string, it should begin with the

element. Any references made in the HTML should be to URL's and not local files since the local path is ambiguous.

## Syntax

"palette_var" is a variable referencing a Palette object.  

```python
# Get the value of the property.
propertyValue = palette_var.htmlFileURL

# Set the value of the property.
palette_var.htmlFileURL = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version March 2017  

