# TextBoxCommandInput.text Property

Parent Object: [TextBoxCommandInput](TextBoxCommandInput.md)  

## Description

Gets and sets the text in the text box. When text is set using the text property, any HTML formatting is ignored and the full string will be displayed in the text box. For example, if you specify the string "Here is a <b>Bold</b> word", and use the formattedText property, you will see "Here is a **Bold** word" in the text box. However, if you use the text property, you will see "Here is a <b>Bold</b> word" and when you get the text property you will get back "Here is a <b>Bold</b> word". This can be useful if you're using the text box to have the user enter HTML code so it's treated as a simple string.

## Syntax

"textBoxCommandInput_var" is a variable referencing a TextBoxCommandInput object.  

```python
# Get the value of the property.
propertyValue = textBoxCommandInput_var.text

# Set the value of the property.
textBoxCommandInput_var.text = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version June 2015  

