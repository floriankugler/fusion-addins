# TextBoxCommandInput.formattedText Property

Parent Object: [TextBoxCommandInput](TextBoxCommandInput.md)  

## Description

Gets and sets the formatted text displayed in the dialog.

## Remarks

Formatted text includes any basic HTML formatting that has been defined. For example, you can use basic HTML formatting such as `Bold`, `Italic`, and ` ` for a line break. It also supports hyper-links, which when clicked by the user, Fusion will open the specified URL in the default browser. Hyper-links are defined using the `` tag such as "`You are using Autodesk's Fusion.`". When setting the formattedText it's assumed the string has HTML formatting and it's best if the TextBoxCommandInput is set the input to be read-only. If the user edits formatted text, the result that's returned by both the formattedText and the text property may not always be as expected. If you want the user to enter or edit text in the text input, then you use the text property to define the text.

## Syntax

"textBoxCommandInput_var" is a variable referencing a TextBoxCommandInput object.  

```python
# Get the value of the property.
propertyValue = textBoxCommandInput_var.formattedText

# Set the value of the property.
textBoxCommandInput_var.formattedText = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version June 2015  

