# SheetMetalRuleValue.expression Property

Parent Object: [SheetMetalRuleValue](SheetMetalRuleValue.md)  

## Description

Gets and sets the expression of the sheet metal rule value. This can be an equation that includes the name "Thickness" and can also include length unit specifiers. For example, a valid expression is "Thickness / 2 + 1 mm". If no units are specified, the unit is implied and uses the units associated with the rule which can be mm or inch. For example an expression of "3" will be 3 inches if the rule units are inches or 3 mm if the rule units are millimeters.

## Syntax

"sheetMetalRuleValue_var" is a variable referencing a SheetMetalRuleValue object.  

```python
# Get the value of the property.
propertyValue = sheetMetalRuleValue_var.expression

# Set the value of the property.
sheetMetalRuleValue_var.expression = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version November 2022  

