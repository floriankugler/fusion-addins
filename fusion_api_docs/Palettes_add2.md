# Palettes.add2 Method

Parent Object: [Palettes](Palettes.md)  

## Description

Creates a new Palette.

## Syntax

"palettes_var" is a variable referencing a [Palettes](Palettes.md) object.

```python
# Uses no optional arguments.
returnValue = palettes_var.add2(id, name, htmlFileURL, isVisible, showCloseButton, isResizable)

# Uses optional arguments.
returnValue = palettes_var.add2(id, name, htmlFileURL, isVisible, showCloseButton, isResizable, width, height)
```

## Return Value

| Type | Description |
|----|----|
| [Palette](Palette.md) | Returns the newly created palette or null in the case the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique id for this palette. The id must be unique with respect to all of the palettes. |
| name | string | The displayed name of this palette. This is the name visible in the user interface. |
| htmlFileURL | string | Specifies the URL to the HTML file that will be displayed in the palette. This can be a local file or a URL on the web where the HTML will be read. To avoid reading a file, this can also be the full HTML definition as a string. If you are providing the HTML content as a string, it should begin with the element. Any references made in the HTML should be to URL's and not local files since the local path is ambiguous. |
| isVisible | boolean | Specifies if the palette is initially visible or not. It's useful to create it invisibly, change other desired properties and then use the isVisible property to finally make it visible to the user. |
| showCloseButton | boolean | Specifies if a "Close" button should be displayed on the palette to allow the user to easily close it. |
| isResizable | boolean | Specifies if the palette can be resized by the user or not. |
| width | integer | Specifies the width of the palette in pixels. If no width is specified a default width will be used. This is an optional argument whose default value is 200. |
| height | integer | Specifies the height of the palette in pixels. If no height is specified a default height will be used. This is an optional argument whose default value is 200. |

## Version

Introduced in version March 2022  

