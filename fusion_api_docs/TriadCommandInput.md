# TriadCommandInput Object

Derived from: [CommandInput](CommandInput.md) Object  

## Description

Represents a command input that displays a triad and allows the user to control translation rotation, and scaling. Using properties on the input you can choose which controls are available to the user. This displays inputs in the command dialog where the user can enter values and also displays a manipulator in the graphics window to allow them to graphically set the values. The input boxes are displayed in the dialog when the isVisible property of the command input is true. The manipulator is displayed in the graphics window when both the isVisible and isEnabled properties are true.  

It will often be useful to first create a GroupCommandInput and then create the TriadCommandInput within the group so it's apparent to the user these items are related and they can be collapsed to reduce clutter in the dialog. This also allows you to label the set of displayed inputs by using the name of the GroupCommandInput.

## Methods

| Name | Description |
|----|----|
| [classType](TriadCommandInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](TriadCommandInput_deleteMe.md) | Deletes this Command input. |
| [hideAll](TriadCommandInput_hideAll.md) | Hides all controls. |
| [hideAllRotations](TriadCommandInput_hideAllRotations.md) | Sets all rotation related controls to be invisible. This is useful if you are only using translations or scaling. |
| [hideAllScaling](TriadCommandInput_hideAllScaling.md) | Sets all scaling related controls to be invisible. This is useful if you are only using translations or rotations. |
| [setFlipVisibility](TriadCommandInput_setFlipVisibility.md) | A convenience method to turn on and off the visibility of the horizontal and vertical flip controls. |
| [setFullVisibility](TriadCommandInput_setFullVisibility.md) | A convenience method to turn on and off the visibility of commonly used controls in a triad. These include the X, Y, and Z axis translations, the X, Y, and Z axis rotations, scaling in the X, Y, and Z directions, scaling on the X-Y, Y-Z and Z-X planes, translation on the X-Y, Y-Z, and Z-X planes, and the origin move. |
| [setPlanarMoveVisibility](TriadCommandInput_setPlanarMoveVisibility.md) | A convenience method to turn on and off the visibility of the X-Y, Y-Z, and Z-X planar translation controls. |
| [setRotateVisibility](TriadCommandInput_setRotateVisibility.md) | A convenience method to turn on and off the visibility of the X, Y, and Z axis rotation controls. |
| [setScaleVisibility](TriadCommandInput_setScaleVisibility.md) | A convenience method to turn on and off the visibility of the controls that define scaling in the X, Y, and Z direction and the X-Y, Y-Z, and Z-X planes. |
| [setTranslateVisibility](TriadCommandInput_setTranslateVisibility.md) | A convenience method to turn on and off the visibility of the X, Y, and Z translation controls. |

## Properties

| Name | Description |
| --- | --- |
| [commandInputs](TriadCommandInput_commandInputs.md) | Gets the CommandInputs class of the parent, which can be a Command, GroupCommandInput or TabCommandInput. |
| [id](TriadCommandInput_id.md) | Gets the unique identifier for this input in the command's CommandInputs. |
| [isEnabled](TriadCommandInput_isEnabled.md) | Gets or sets if this input is currently enabled or disabled for user interaction. Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property. |
| [isFlippedHorizontal](TriadCommandInput_isFlippedHorizontal.md) | Gets and sets if the triad is flipped horizontally (around the around the Y-Z plane of the triad). |
| [isFlippedVertical](TriadCommandInput_isFlippedVertical.md) | Gets and sets if the triad is flipped vertically (around the around the X-Z plane of the triad). |
| [isFullWidth](TriadCommandInput_isFullWidth.md) | Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs. |
| [isHorizontalFlipVisible](TriadCommandInput_isHorizontalFlipVisible.md) | Gets and sets if the control that lets the user flip horizontally (around the Y-Z plane of the triad) is visible in both the graphical manipulator and the dialog. |
| [isOriginTranslationVisible](TriadCommandInput_isOriginTranslationVisible.md) | Gets and sets if the control that supports translation in the X, Y, and Z directions is visible in both the graphical manipulator and in the dialog. In the manipulator, this is the large dot at the origin or the triad. |
| [isUnifiedScalingVisible](TriadCommandInput_isUnifiedScalingVisible.md) | Gets and sets if the control that defines the scaling in all directions visible in both the graphical manipulator and in the dialog. |
| [isValid](TriadCommandInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isValidExpressions](TriadCommandInput_isValidExpressions.md) | Returns true if all of the input fields have valid expressions. If this property is false, the triad is incorrectly defined and the current values should not be used. |
| [isVerticalFlipVisible](TriadCommandInput_isVerticalFlipVisible.md) | Gets and sets if the control that lets the user flip vertical (around the X-Z plane of the triad) is visible in both the graphical manipulator and the dialog. |
| [isVisible](TriadCommandInput_isVisible.md) | Gets or sets if this input will be visible to the user. Setting a SelectionCommandInput to be invisible will clear any selections it currently has. |
| [isXRotationVisible](TriadCommandInput_isXRotationVisible.md) | Gets and sets if the control that defines the rotation around the X axis is visible in both the graphical manipulator and in the dialog. |
| [isXScalingInXYVisible](TriadCommandInput_isXScalingInXYVisible.md) | Gets and sets if the control that defines the scaling along the X axis is visible in both the graphical manipulator and in the dialog. This control lies on the X-Y plane of the triad. |
| [isXScalingInXZVisible](TriadCommandInput_isXScalingInXZVisible.md) | Gets and sets if the control that defines the scaling along the X axis is visible in both the graphical manipulator and in the dialog. This control lies on the X-Z plane of the triad. |
| [isXTranslationVisible](TriadCommandInput_isXTranslationVisible.md) | Gets and sets if the control that supports X Translation is visible in both the graphical manipulator and in the dialog. |
| [isXYPlaneScalingVisible](TriadCommandInput_isXYPlaneScalingVisible.md) | Gets and sets if the control that defines the scaling in the X-Y plane is visible in both the graphical manipulator and in the dialog. |
| [isXYPlaneTranslationVisible](TriadCommandInput_isXYPlaneTranslationVisible.md) | Gets and sets if the control that defines the translation in the X-Y plane is visible in both the graphical manipulator and in the dialog. |
| [isXZPlaneScalingVisible](TriadCommandInput_isXZPlaneScalingVisible.md) | Gets and sets if the control that defines the scaling in the X-Z plane is visible in both the graphical manipulator and in the dialog. |
| [isXZPlaneTranslationVisible](TriadCommandInput_isXZPlaneTranslationVisible.md) | Gets and sets if the control that defines the translation in the X-Z plane is visible in both the graphical manipulator and in the dialog. |
| [isYRotationVisible](TriadCommandInput_isYRotationVisible.md) | Gets and sets if the control that defines the rotation around the Y axis is visible in both the graphical manipulator and in the dialog. |
| [isYScalingInXYVisible](TriadCommandInput_isYScalingInXYVisible.md) | Gets and sets if the control that defines the scaling along the Y axis is visible in both the graphical manipulator and in the dialog. This control lies on the X-Y plane of the triad. |
| [isYScalingInYZVisible](TriadCommandInput_isYScalingInYZVisible.md) | Gets and sets if the control that defines the scaling along the Y axis is visible in both the graphical manipulator and in the dialog. This control lies on the Y-Z plane of the triad. |
| [isYTranslationVisible](TriadCommandInput_isYTranslationVisible.md) | Gets and sets if the control that defines the Y Translation is visible in both the graphical manipulator and in the dialog. |
| [isYZPlaneScalingVisible](TriadCommandInput_isYZPlaneScalingVisible.md) | Gets and sets if the control that defines the scaling in the Y-Z plane is visible in both the graphical manipulator and in the dialog. |
| [isYZPlaneTranslationVisible](TriadCommandInput_isYZPlaneTranslationVisible.md) | Gets and sets if the control that defines the translation in the Y-Z plane is visible in both the graphical manipulator and in the dialog. |
| [isZRotationVisible](TriadCommandInput_isZRotationVisible.md) | Gets and sets if the control that defines the rotation around the Z axis is visible in both the graphical manipulator and in the dialog. |
| [isZScalingInXZVisible](TriadCommandInput_isZScalingInXZVisible.md) | Gets and sets if the control that defines the scaling along the Z axis is visible in both the graphical manipulator and in the dialog. This control lies on the X-Z plane of the triad. |
| [isZScalingInYZVisible](TriadCommandInput_isZScalingInYZVisible.md) | Gets and sets if the control that defines the scaling along the Z axis is visible in both the graphical manipulator and in the dialog. This control lies on the Y-Z plane of the triad. |
| [isZTranslationVisible](TriadCommandInput_isZTranslationVisible.md) | Gets and sets if the control that defines the Z Translation is visible in both the graphical manipulator and in the dialog. |
| [lastChangeMade](TriadCommandInput_lastChangeMade.md) | Returns which value was most recently changed. To determine the actual change made you need to compare the transforms returned by the transform and lastTransform properties. Having information about the specific type of change made makes it easier to compare the matrices because you know what to look for. |
| [lastTransform](TriadCommandInput_lastTransform.md) | Returns the transform of the triad before the latest change. Using the matrices returned by this property and the transform property you can determine what changed. The lastChangeMade property is also useful to help you know the type of change to look for when comparing the matrices. |
| [name](TriadCommandInput_name.md) | Gets the user visible name of this input. |
| [objectType](TriadCommandInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCommand](TriadCommandInput_parentCommand.md) | Gets the parent Command. |
| [parentCommandInput](TriadCommandInput_parentCommandInput.md) | Gets the parent CommandInput if this commandInput is the child of a TabCommandInput or GroupCommandInput. Returns null if there is no parent. |
| [positionTransform](TriadCommandInput_positionTransform.md) | Gets the current position and orientation of the triad using a transformation matrix. This transform does not include any scaling. |
| [toolClipFilename](TriadCommandInput_toolClipFilename.md) | Gets or sets the full filename of the image file (PNG) used for the tool clip. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [tooltip](TriadCommandInput_tooltip.md) | Gets or sets the base tooltip string. This is always shown for commands. If the tooltip description and/or tool clip are also specified then the tooltip will progressively display more information as the user hovers the mouse over the control. |
| [tooltipDescription](TriadCommandInput_tooltipDescription.md) | Gets or sets additional text to display progressively along with the tooltip. The text for the description can contain some basic HTML formatting tags to format the tags. For example the br tag can be used to create multiple paragraphs. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [transform](TriadCommandInput_transform.md) | Gets or sets the current position, orientation, and scale of the triad using a transformation matrix. |
| [unifiedeScaleFactor](TriadCommandInput_unifiedeScaleFactor.md) | Gets and sets the current value of the unified scale factor of the triad. The isValidExpressions property should be checked before using the value within the command. |
| [unifiedScaleFactorExpression](TriadCommandInput_unifiedScaleFactorExpression.md) | Gets or sets the expression displayed in the input field for the unified scale. This can contain equations and references to parameters but must result in a valid unitless expression. |
| [xRotation](TriadCommandInput_xRotation.md) | Gets and sets the current value of the rotation around the X axis of the triad. The value is in radians but will be displayed to the user in degrees. The isValidExpressions property should be checked before using the value within the command. |
| [xRotationExpression](TriadCommandInput_xRotationExpression.md) | Gets or sets the expression displayed in the input field for the X rotation. This can contain equations and references to parameters but must result in a valid distance expression. If units are not specified as part of the expression degrees are used. |
| [xScaleFactor](TriadCommandInput_xScaleFactor.md) | Gets and sets the current value of the scale factor along the X axis of the triad. The isValidExpressions property should be checked before using the value within the command. |
| [xScaleFactorExpression](TriadCommandInput_xScaleFactorExpression.md) | Gets or sets the expression displayed in the input field for the X scale. This can contain equations and references to parameters but must result in a valid unitless expression. |
| [xTranslation](TriadCommandInput_xTranslation.md) | Gets and sets the current value of the translation along the X axis of the triad. The value is in centimeters but will be displayed to the user in default units for the design. The isValidExpressions property should be checked before using the returned value. |
| [xTranslationExpression](TriadCommandInput_xTranslationExpression.md) | Gets or sets the expression displayed in the input field for the X translation. This can contain equations and references to parameters but must result in a valid distance expression. If units are not specified as part of the expression, the default user units of length are used. |
| [xYPlaneScaleFactor](TriadCommandInput_xYPlaneScaleFactor.md) | Gets and sets the current value of the scale factor on the X-Y plane of the triad. The isValidExpressions property should be checked before using the value within the command. |
| [xYPlaneScaleFactorExpression](TriadCommandInput_xYPlaneScaleFactorExpression.md) | Gets or sets the expression displayed in the input field for the X-Y plane scale. This can contain equations and references to parameters but must result in a valid unitless expression. |
| [yRotation](TriadCommandInput_yRotation.md) | Gets and sets the current value of the rotation around the Y axis of the triad. The value is in radians but will be displayed to the user in degrees. The isValidExpressions property should be checked before using the value within the command. |
| [yRotationExpression](TriadCommandInput_yRotationExpression.md) | Gets or sets the expression displayed in the input field for the Y rotation. This can contain equations and references to parameters but must result in a valid distance expression. If units are not specified as part of the expression degrees are used. |
| [yScaleFactor](TriadCommandInput_yScaleFactor.md) | Gets and sets the current value of the scale factor along the Y axis of the triad. The isValidExpressions property should be checked before using the value within the command. |
| [yScaleFactorExpression](TriadCommandInput_yScaleFactorExpression.md) | Gets or sets the expression displayed in the input field for the Y scale. This can contain equations and references to parameters but must result in a valid unitless expression. |
| [yTranslation](TriadCommandInput_yTranslation.md) | Gets and sets the current value of the translation along the Y axis of the triad. The value is in centimeters but will be displayed to the user in default units for the design. The isValidExpressions property should be checked before using the value within the command. |
| [yTranslationExpression](TriadCommandInput_yTranslationExpression.md) | Gets or sets the expression displayed in the input field for the Y translation. This can contain equations and references to parameters but must result in a valid distance expression. If units are not specified as part of the expression, the default user units of length are used. |
| [yZPlaneScaleFactor](TriadCommandInput_yZPlaneScaleFactor.md) | Gets and sets the current value of the scale factor on the Y-Z plane of the triad. The isValidExpressions property should be checked before using the value within the command. |
| [yZPlaneScaleFactorExpression](TriadCommandInput_yZPlaneScaleFactorExpression.md) | Gets or sets the expression displayed in the input field for the Y-Z plane scale. This can contain equations and references to parameters but must result in a valid unitless expression. |
| [zRotation](TriadCommandInput_zRotation.md) | Gets and sets the current value of the rotation around the Z axis of the triad. The value is in radians but will be displayed to the user in degrees. The isValidExpressions property should be checked before using the value within the command. |
| [zRotationExpression](TriadCommandInput_zRotationExpression.md) | Gets or sets the expression displayed in the input field for the Z rotation. This can contain equations and references to parameters but must result in a valid distance expression. If units are not specified as part of the expression degrees are used. |
| [zScaleFactor](TriadCommandInput_zScaleFactor.md) | Gets and sets the current value of the scale factor along the Z axis of the triad. The isValidExpressions property should be checked before using the value within the command. |
| [zScaleFactorExpression](TriadCommandInput_zScaleFactorExpression.md) | Gets or sets the expression displayed in the input field for the Z scale. This can contain equations and references to parameters but must result in a valid unitless expression. |
| [zTranslation](TriadCommandInput_zTranslation.md) | Gets and sets the current value of the translation along the Z axis of the triad. The value is in centimeters but will be displayed to the user in default units for the design. The isValidExpressions property should be checked before using the value within the command. |
| [zTranslationExpression](TriadCommandInput_zTranslationExpression.md) | Gets or sets the expression displayed in the input field for the Z translation. This can contain equations and references to parameters but must result in a valid distance expression. If units are not specified as part of the expression, the default user units of length are used. |
| [zXPlaneScaleFactor](TriadCommandInput_zXPlaneScaleFactor.md) | Gets and sets the current value of the scale factor on the Z-X plane of the triad. The isValidExpressions property should be checked before using the value within the command. |
| [zXPlaneScaleFactorExpression](TriadCommandInput_zXPlaneScaleFactorExpression.md) | Gets or sets the expression displayed in the input field for the Z-X plane scale. This can contain equations and references to parameters but must result in a valid unitless expression. |

## Accessed From

[CommandInputs.addTriadCommandInput](CommandInputs_addTriadCommandInput.md)

## Version

Introduced in version May 2022  

