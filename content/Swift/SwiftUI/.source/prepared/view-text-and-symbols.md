# Text and symbol modifiers

Manage the rendering, selection, and entry of text in your view.

## Overview {#Overview}

SwiftUI provides built-in views that display text to the user, like [Text](https://developer.apple.com/documentation/swiftui/text) and [Label](https://developer.apple.com/documentation/swiftui/label), or that collect text from the user, like [TextField](https://developer.apple.com/documentation/swiftui/textfield) and [TextEditor](https://developer.apple.com/documentation/swiftui/texteditor). Use text and symbol modifiers to control how SwiftUI displays and manages that text. For example, you can set a font, specify text layout parameters, and indicate what kind of input to expect.

To learn more about the kinds of views that you use to display text and the ways in which you can configure those views, see [Text input and output](../../5-TextInputAndOutput/).

## Fonts {#Fonts}

- [font(_:)](https://developer.apple.com/documentation/swiftui/view/font(_:)) — Sets the default font for text in this view.

## Dynamic type {#Dynamic-type}

- [dynamicTypeSize(_:)](https://developer.apple.com/documentation/swiftui/view/dynamictypesize(_:)) — Sets the Dynamic Type size within the view to the given value.

## Text style {#Text-style}

- [bold(_:)](https://developer.apple.com/documentation/swiftui/view/bold(_:)) — Applies a bold font weight to the text in this view.
- [fontDesign(_:)](https://developer.apple.com/documentation/swiftui/view/fontdesign(_:)) — Sets the font design of the text in this view.
- [fontWeight(_:)](https://developer.apple.com/documentation/swiftui/view/fontweight(_:)) — Sets the font weight of the text in this view.
- [fontWidth(_:)](https://developer.apple.com/documentation/swiftui/view/fontwidth(_:)) — Sets the font width of the text in this view.
- [italic(_:)](https://developer.apple.com/documentation/swiftui/view/italic(_:)) — Applies italics to the text in this view.
- [monospaced(_:)](https://developer.apple.com/documentation/swiftui/view/monospaced(_:)) — Modifies the fonts of all child views to use the fixed-width variant of the current font, if possible.
- [monospacedDigit()](https://developer.apple.com/documentation/swiftui/view/monospaceddigit()) — Modifies the fonts of all child views to use fixed-width digits, if possible, while leaving other characters proportionally spaced.
- [strikethrough(_:pattern:color:)](https://developer.apple.com/documentation/swiftui/view/strikethrough(_:pattern:color:)) — Applies a strikethrough to the text in this view.
- [textCase(_:)](https://developer.apple.com/documentation/swiftui/view/textcase(_:)) — Sets a transform for the case of the text contained in this view when displayed.
- [textScale(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/textscale(_:isenabled:)) — Applies a text scale to text in the view.
- [textRenderer(_:)](https://developer.apple.com/documentation/swiftui/view/textrenderer(_:)) — Returns a new view such that any text views within it will use `renderer` to draw themselves.
- [underline(_:pattern:color:)](https://developer.apple.com/documentation/swiftui/view/underline(_:pattern:color:)) — Applies an underline to the text in this view.
- [attributedTextFormattingDefinition(_:)](https://developer.apple.com/documentation/swiftui/view/attributedtextformattingdefinition(_:)) — Apply a text formatting definition to nested views.

## Label configuration {#Label-configuration}

- [labelIconToTitleSpacing(_:)](https://developer.apple.com/documentation/swiftui/view/labelicontotitlespacing(_:)) — Set the spacing between the icon and title in labels.
- [labelReservedIconWidth(_:)](https://developer.apple.com/documentation/swiftui/view/labelreservediconwidth(_:)) — Set the width reserved for icons in labels.

## Text layout {#Text-layout}

- [allowsTightening(_:)](https://developer.apple.com/documentation/swiftui/view/allowstightening(_:)) — Sets whether text in this view can compress the space between characters when necessary to fit text in a line.
- [baselineOffset(_:)](https://developer.apple.com/documentation/swiftui/view/baselineoffset(_:)) — Sets the vertical offset for the text relative to its baseline in this view.
- [flipsForRightToLeftLayoutDirection(_:)](https://developer.apple.com/documentation/swiftui/view/flipsforrighttoleftlayoutdirection(_:)) — Sets whether this view mirrors its contents horizontally when the layout direction is right-to-left.
- [kerning(_:)](https://developer.apple.com/documentation/swiftui/view/kerning(_:)) — Sets the spacing, or kerning, between characters for the text in this view.
- [lineHeight(_:)](https://developer.apple.com/documentation/swiftui/view/lineheight(_:)) — A modifier for the default line height in the view hierarchy.
- [minimumScaleFactor(_:)](https://developer.apple.com/documentation/swiftui/view/minimumscalefactor(_:)) — Sets the minimum amount that text in this view scales down to fit in the available space.
- [tracking(_:)](https://developer.apple.com/documentation/swiftui/view/tracking(_:)) — Sets the tracking for the text in this view.
- [truncationMode(_:)](https://developer.apple.com/documentation/swiftui/view/truncationmode(_:)) — Sets the truncation mode for lines of text that are too long to fit in the available space.
- [typesettingLanguage(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/typesettinglanguage(_:isenabled:)) — Specifies the language for typesetting.
- [writingDirection(strategy:)](https://developer.apple.com/documentation/swiftui/view/writingdirection(strategy:)) — A modifier for the default text writing direction strategy in the view hierarchy.

## Multiline text {#Multiline-text}

- [lineLimit(_:)](https://developer.apple.com/documentation/swiftui/view/linelimit(_:)) — Sets to a closed range the number of lines that text can occupy in this view.
- [lineLimit(_:reservesSpace:)](https://developer.apple.com/documentation/swiftui/view/linelimit(_:reservesspace:)) — Sets a limit for the number of lines text can occupy in this view.
- [lineSpacing(_:)](https://developer.apple.com/documentation/swiftui/view/linespacing(_:)) — Sets the amount of space between lines of text in this view.
- [multilineTextAlignment(_:)](https://developer.apple.com/documentation/swiftui/view/multilinetextalignment(_:)) — Sets the alignment of a text view that contains multiple lines of text.
- [multilineTextAlignment(strategy:)](https://developer.apple.com/documentation/swiftui/view/multilinetextalignment(strategy:)) — A modifier for the default text alignment strategy in the view hierarchy.

## Text selection {#Text-selection}

- [textSelection(_:)](https://developer.apple.com/documentation/swiftui/view/textselection(_:)) — Controls whether people can select text within this view.
- [textSelectionAffinity(_:)](https://developer.apple.com/documentation/swiftui/view/textselectionaffinity(_:)) — Sets the direction of a selection or cursor relative to a text character.

## Data detection {#Data-detection}

- [dataDetection(_:options:)](https://developer.apple.com/documentation/swiftui/view/datadetection(_:options:)) — Asynchronously detects data in the view’s content and styles them to indicate they are clickable.

## Text entry {#Text-entry}

- [autocorrectionDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/autocorrectiondisabled(_:)) — Sets whether to disable autocorrection for this view.
- [keyboardType(_:)](https://developer.apple.com/documentation/swiftui/view/keyboardtype(_:)) — Sets the keyboard type for this view.
- [scrollDismissesKeyboard(_:)](https://developer.apple.com/documentation/swiftui/view/scrolldismisseskeyboard(_:)) — Configures the behavior in which scrollable content interacts with the software keyboard.
- [textInputAutocapitalization(_:)](https://developer.apple.com/documentation/swiftui/view/textinputautocapitalization(_:)) — Sets how often the shift key in the keyboard is automatically enabled.
- [textInputBorderShape(_:)](https://developer.apple.com/documentation/swiftui/view/textinputbordershape(_:)) — Sets the border shape for text input controls in the view hierarchy.
- [textInputCompletion(_:)](https://developer.apple.com/documentation/swiftui/view/textinputcompletion(_:)) — Associates a fully formed string with the value of this view when used as a text input suggestion
- [textInputSuggestions(_:)](https://developer.apple.com/documentation/swiftui/view/textinputsuggestions(_:)) — Configures the text input suggestions for this view.
- [textInputSuggestions(_:content:)](https://developer.apple.com/documentation/swiftui/view/textinputsuggestions(_:content:)) — Configures the text input suggestions for this view.
- [textInputSuggestions(_:id:content:)](https://developer.apple.com/documentation/swiftui/view/textinputsuggestions(_:id:content:)) — Configures the text input suggestions for this view.
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)) — Sets the text content type for this view, which the system uses to offer suggestions while the user enters text on macOS.
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)-4dqqb) — Sets the text content type for this view, which the system uses to offer suggestions while the user enters text on a watchOS device.
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)-6fic1) — Sets the text content type for this view, which the system uses to offer suggestions while the user enters text on macOS.
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)-ufdv) — Sets the text content type for this view, which the system uses to offer suggestions while the user enters text on an iOS or tvOS device.
- [textInputFormattingControlVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/textinputformattingcontrolvisibility(_:for:)) — Specifies which system text formatting controls are available for people to format text.

## Find and replace {#Find-and-replace}

- [findNavigator(isPresented:)](https://developer.apple.com/documentation/swiftui/view/findnavigator(ispresented:)) — Programmatically presents the find and replace interface for text editor views.
- [findDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/finddisabled(_:)) — Prevents find and replace operations in a text editor.
- [replaceDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/replacedisabled(_:)) — Prevents replace operations in a text editor.

## Symbol appearance {#Symbol-appearance}

- [symbolRenderingMode(_:)](https://developer.apple.com/documentation/swiftui/view/symbolrenderingmode(_:)) — Sets the rendering mode for symbol images within this view.
- [symbolColorRenderingMode(_:)](https://developer.apple.com/documentation/swiftui/view/symbolcolorrenderingmode(_:)) — Sets the color rendering mode for symbol images.
- [symbolVariableValueMode(_:)](https://developer.apple.com/documentation/swiftui/view/symbolvariablevaluemode(_:)) — Sets the variable value mode mode for symbol images within this view.
- [symbolVariant(_:)](https://developer.apple.com/documentation/swiftui/view/symbolvariant(_:)) — Makes symbols within the view show a particular variant.

## Writing Tools {#Writing-Tools}

- [writingToolsAffordanceVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/writingtoolsaffordancevisibility(_:)) — Specifies whether the system should show the Writing Tools affordance for text input views affected by the environment.
- [writingToolsBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/writingtoolsbehavior(_:)) — Specifies the Writing Tools behavior for text and text input in the environment.
- [WritingToolsBehavior](https://developer.apple.com/documentation/swiftui/writingtoolsbehavior) — The Writing Tools editing experience for text and text input.
