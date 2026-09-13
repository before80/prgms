# Text input and output

Display formatted text and get text input from the user.

## Overview {#Overview}

To display read-only text, or read-only text paired with an image, use the built-in [Text](https://developer.apple.com/documentation/swiftui/text) or [Label](https://developer.apple.com/documentation/swiftui/label) views, respectively. When you need to collect text input from the user, use an appropriate text input view, like [TextField](https://developer.apple.com/documentation/swiftui/textfield) or [TextEditor](https://developer.apple.com/documentation/swiftui/texteditor).

![](./images/text-input-and-output-hero@2x.png)

You add view modifiers to control the text’s font, selectability, alignment, layout direction, and so on. These modifiers also affect other views that display text, like the labels on controls, even if you don’t define an explicit [Text](https://developer.apple.com/documentation/swiftui/text) view.

For design guidance, see [Typography](https://developer.apple.com/design/human-interface-guidelines/typography) in the Human Interface Guidelines.

## Displaying text {#Displaying-text}

- [Text](https://developer.apple.com/documentation/swiftui/text) — A view that displays one or more lines of read-only text.
- [Label](https://developer.apple.com/documentation/swiftui/label) — A standard label for user interface items, consisting of an icon with a title.
- [labelStyle(_:)](https://developer.apple.com/documentation/swiftui/view/labelstyle(_:)) — Sets the style for labels within this view.

## Getting text input {#Getting-text-input}

- [Building rich SwiftUI text experiences](5.1-BuildingRichSwiftuiTextExperiences/) — Build an editor for formatted text using SwiftUI text editor views and attributed strings.
- [TextField](https://developer.apple.com/documentation/swiftui/textfield) — A control that displays an editable text interface.
- [textFieldStyle(_:)](https://developer.apple.com/documentation/swiftui/view/textfieldstyle(_:)) — Sets the style for text fields within this view.
- [SecureField](https://developer.apple.com/documentation/swiftui/securefield) — A control into which people securely enter private text.
- [TextEditor](https://developer.apple.com/documentation/swiftui/texteditor) — A view that can display and edit long-form text.

## Selecting text {#Selecting-text}

- [textSelection(_:)](https://developer.apple.com/documentation/swiftui/view/textselection(_:)) — Controls whether people can select text within this view.
- [TextSelectability](https://developer.apple.com/documentation/swiftui/textselectability) — A type that describes the ability to select text.
- [TextSelection](https://developer.apple.com/documentation/swiftui/textselection) — Represents a selection of text.
- [textSelectionAffinity(_:)](https://developer.apple.com/documentation/swiftui/view/textselectionaffinity(_:)) — Sets the direction of a selection or cursor relative to a text character.
- [textSelectionAffinity](https://developer.apple.com/documentation/swiftui/environmentvalues/textselectionaffinity) — A representation of the direction or association of a selection or cursor relative to a text character. This concept becomes much more prominent when dealing with bidirectional text (text that contains both LTR and RTL scripts, like English and Arabic combined).
- [TextSelectionAffinity](https://developer.apple.com/documentation/swiftui/textselectionaffinity) — A representation of the direction or association of a selection or cursor relative to a text character. This concept becomes much more prominent when dealing with bidirectional text (text that contains both LTR and RTL scripts, like English and Arabic combined).
- [AttributedTextSelection](https://developer.apple.com/documentation/swiftui/attributedtextselection) — Represents a selection of attributed text.

## Setting a font {#Setting-a-font}

- [Applying custom fonts to text](5.3-ApplyingCustomFontsToText/) — Add and use a font in your app that scales with Dynamic Type.
- [font(_:)](https://developer.apple.com/documentation/swiftui/view/font(_:)) — Sets the default font for text in this view.
- [fontDesign(_:)](https://developer.apple.com/documentation/swiftui/view/fontdesign(_:)) — Sets the font design of the text in this view.
- [fontWeight(_:)](https://developer.apple.com/documentation/swiftui/view/fontweight(_:)) — Sets the font weight of the text in this view.
- [fontWidth(_:)](https://developer.apple.com/documentation/swiftui/view/fontwidth(_:)) — Sets the font width of the text in this view.
- [font](https://developer.apple.com/documentation/swiftui/environmentvalues/font) — The default font of this environment.
- [Font](https://developer.apple.com/documentation/swiftui/font) — An environment-dependent font.

## Adjusting text size {#Adjusting-text-size}

- [textScale(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/textscale(_:isenabled:)) — Applies a text scale to text in the view.
- [dynamicTypeSize(_:)](https://developer.apple.com/documentation/swiftui/view/dynamictypesize(_:)) — Sets the Dynamic Type size within the view to the given value.
- [dynamicTypeSize](https://developer.apple.com/documentation/swiftui/environmentvalues/dynamictypesize) — The current Dynamic Type size.
- [DynamicTypeSize](https://developer.apple.com/documentation/swiftui/dynamictypesize) — A Dynamic Type size, which specifies how large scalable content should be.
- [ScaledMetric](https://developer.apple.com/documentation/swiftui/scaledmetric) — A dynamic property that scales a numeric value.
- [TextVariantPreference](https://developer.apple.com/documentation/swiftui/textvariantpreference) — A protocol for controlling the size variant of text views.
- [FixedTextVariant](https://developer.apple.com/documentation/swiftui/fixedtextvariant) — The default text variant preference that chooses the largest available variant.
- [SizeDependentTextVariant](https://developer.apple.com/documentation/swiftui/sizedependenttextvariant) — The size dependent variant preference allows the text to take the available space into account when choosing the variant to display.

## Controlling text style {#Controlling-text-style}

- [bold(_:)](https://developer.apple.com/documentation/swiftui/view/bold(_:)) — Applies a bold font weight to the text in this view.
- [italic(_:)](https://developer.apple.com/documentation/swiftui/view/italic(_:)) — Applies italics to the text in this view.
- [underline(_:pattern:color:)](https://developer.apple.com/documentation/swiftui/view/underline(_:pattern:color:)) — Applies an underline to the text in this view.
- [strikethrough(_:pattern:color:)](https://developer.apple.com/documentation/swiftui/view/strikethrough(_:pattern:color:)) — Applies a strikethrough to the text in this view.
- [textCase(_:)](https://developer.apple.com/documentation/swiftui/view/textcase(_:)) — Sets a transform for the case of the text contained in this view when displayed.
- [textCase](https://developer.apple.com/documentation/swiftui/environmentvalues/textcase) — A stylistic override to transform the case of `Text` when displayed, using the environment’s locale.
- [monospaced(_:)](https://developer.apple.com/documentation/swiftui/view/monospaced(_:)) — Modifies the fonts of all child views to use the fixed-width variant of the current font, if possible.
- [monospacedDigit()](https://developer.apple.com/documentation/swiftui/view/monospaceddigit()) — Modifies the fonts of all child views to use fixed-width digits, if possible, while leaving other characters proportionally spaced.
- [AttributedTextFormattingDefinition](https://developer.apple.com/documentation/swiftui/attributedtextformattingdefinition) — A protocol for defining how text can be styled in a view.
- [AttributedTextValueConstraint](https://developer.apple.com/documentation/swiftui/attributedtextvalueconstraint) — A protocol for defining a constraint on the value of a certain attribute.
- [AttributedTextFormatting](https://developer.apple.com/documentation/swiftui/attributedtextformatting) — A namespace for types related to attributed text formatting definitions.

## Managing text layout {#Managing-text-layout}

- [truncationMode(_:)](https://developer.apple.com/documentation/swiftui/view/truncationmode(_:)) — Sets the truncation mode for lines of text that are too long to fit in the available space.
- [truncationMode](https://developer.apple.com/documentation/swiftui/environmentvalues/truncationmode) — A value that indicates how the layout truncates the last line of text to fit into the available space.
- [allowsTightening(_:)](https://developer.apple.com/documentation/swiftui/view/allowstightening(_:)) — Sets whether text in this view can compress the space between characters when necessary to fit text in a line.
- [allowsTightening](https://developer.apple.com/documentation/swiftui/environmentvalues/allowstightening) — A Boolean value that indicates whether inter-character spacing should tighten to fit the text into the available space.
- [minimumScaleFactor(_:)](https://developer.apple.com/documentation/swiftui/view/minimumscalefactor(_:)) — Sets the minimum amount that text in this view scales down to fit in the available space.
- [minimumScaleFactor](https://developer.apple.com/documentation/swiftui/environmentvalues/minimumscalefactor) — The minimum permissible proportion to shrink the font size to fit the text into the available space.
- [baselineOffset(_:)](https://developer.apple.com/documentation/swiftui/view/baselineoffset(_:)) — Sets the vertical offset for the text relative to its baseline in this view.
- [kerning(_:)](https://developer.apple.com/documentation/swiftui/view/kerning(_:)) — Sets the spacing, or kerning, between characters for the text in this view.
- [tracking(_:)](https://developer.apple.com/documentation/swiftui/view/tracking(_:)) — Sets the tracking for the text in this view.
- [flipsForRightToLeftLayoutDirection(_:)](https://developer.apple.com/documentation/swiftui/view/flipsforrighttoleftlayoutdirection(_:)) — Sets whether this view mirrors its contents horizontally when the layout direction is right-to-left.
- [TextAlignment](https://developer.apple.com/documentation/swiftui/textalignment) — An alignment position for text along the horizontal axis.

## Rendering text {#Rendering-text}

- [Creating visual effects with SwiftUI](5.4-CreatingVisualEffectsWithSwiftui/) — Add scroll effects, rich color treatments, custom transitions, and advanced effects using shaders and a text renderer.
- [TextAttribute](https://developer.apple.com/documentation/swiftui/textattribute) — A value that you can attach to text views and that text renderers can query.
- [textRenderer(_:)](https://developer.apple.com/documentation/swiftui/view/textrenderer(_:)) — Returns a new view such that any text views within it will use `renderer` to draw themselves.
- [TextRenderer](https://developer.apple.com/documentation/swiftui/textrenderer) — A value that can replace the default text view rendering behavior.
- [TextProxy](https://developer.apple.com/documentation/swiftui/textproxy) — A proxy for a text view that custom text renderers use.

## Limiting line count for multiline text {#Limiting-line-count-for-multiline-text}

- [lineLimit(_:)](https://developer.apple.com/documentation/swiftui/view/linelimit(_:)) — Sets to a closed range the number of lines that text can occupy in this view.
- [lineLimit(_:reservesSpace:)](https://developer.apple.com/documentation/swiftui/view/linelimit(_:reservesspace:)) — Sets a limit for the number of lines text can occupy in this view.
- [lineLimit](https://developer.apple.com/documentation/swiftui/environmentvalues/linelimit) — The maximum number of lines that text can occupy in a view.

## Formatting multiline text {#Formatting-multiline-text}

- [lineSpacing(_:)](https://developer.apple.com/documentation/swiftui/view/linespacing(_:)) — Sets the amount of space between lines of text in this view.
- [lineSpacing](https://developer.apple.com/documentation/swiftui/environmentvalues/linespacing) — The distance in points between the bottom of one line fragment and the top of the next.
- [multilineTextAlignment(_:)](https://developer.apple.com/documentation/swiftui/view/multilinetextalignment(_:)) — Sets the alignment of a text view that contains multiple lines of text.
- [multilineTextAlignment](https://developer.apple.com/documentation/swiftui/environmentvalues/multilinetextalignment) — An environment value that indicates how a text view aligns its lines when the content wraps or contains newlines.

## Formatting date and time {#Formatting-date-and-time}

- [SystemFormatStyle](https://developer.apple.com/documentation/swiftui/systemformatstyle) — A collection of format styles for displaying live-updating time information in text views.
- [TimeDataSource](https://developer.apple.com/documentation/swiftui/timedatasource) — A source of time related data.

## Managing text entry {#Managing-text-entry}

- [autocorrectionDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/autocorrectiondisabled(_:)) — Sets whether to disable autocorrection for this view.
- [autocorrectionDisabled](https://developer.apple.com/documentation/swiftui/environmentvalues/autocorrectiondisabled) — A Boolean value that determines whether the view hierarchy has auto-correction enabled.
- [keyboardType(_:)](https://developer.apple.com/documentation/swiftui/view/keyboardtype(_:)) — Sets the keyboard type for this view.
- [scrollDismissesKeyboard(_:)](https://developer.apple.com/documentation/swiftui/view/scrolldismisseskeyboard(_:)) — Configures the behavior in which scrollable content interacts with the software keyboard.
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)) — Sets the text content type for this view, which the system uses to offer suggestions while the user enters text on macOS.
- [textInputAutocapitalization(_:)](https://developer.apple.com/documentation/swiftui/view/textinputautocapitalization(_:)) — Sets how often the shift key in the keyboard is automatically enabled.
- [TextInputAutocapitalization](https://developer.apple.com/documentation/swiftui/textinputautocapitalization) — The kind of autocapitalization behavior applied during text input.
- [textInputBorderShape(_:)](https://developer.apple.com/documentation/swiftui/view/textinputbordershape(_:)) — Sets the border shape for text input controls in the view hierarchy.
- [TextInputBorderShape](https://developer.apple.com/documentation/swiftui/textinputbordershape) — A shape used to draw the border of a text input control.
- [textInputCompletion(_:)](https://developer.apple.com/documentation/swiftui/view/textinputcompletion(_:)) — Associates a fully formed string with the value of this view when used as a text input suggestion
- [textInputSuggestions(_:)](https://developer.apple.com/documentation/swiftui/view/textinputsuggestions(_:)) — Configures the text input suggestions for this view.
- [textInputSuggestions(_:content:)](https://developer.apple.com/documentation/swiftui/view/textinputsuggestions(_:content:)) — Configures the text input suggestions for this view.
- [textInputSuggestions(_:id:content:)](https://developer.apple.com/documentation/swiftui/view/textinputsuggestions(_:id:content:)) — Configures the text input suggestions for this view.
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)-4dqqb) — Sets the text content type for this view, which the system uses to offer suggestions while the user enters text on a watchOS device.
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)-6fic1) — Sets the text content type for this view, which the system uses to offer suggestions while the user enters text on macOS.
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)-ufdv) — Sets the text content type for this view, which the system uses to offer suggestions while the user enters text on an iOS or tvOS device.
- [textInputFormattingControlVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/textinputformattingcontrolvisibility(_:for:)) — Specifies which system text formatting controls are available for people to format text.
- [TextInputFormattingControlPlacement](https://developer.apple.com/documentation/swiftui/textinputformattingcontrolplacement) — A structure defining the system text formatting controls available on each platform.

## Dictating text {#Dictating-text}

- [searchDictationBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/searchdictationbehavior(_:)) — Configures the dictation behavior for any search fields configured by the searchable modifier.
- [TextInputDictationActivation](https://developer.apple.com/documentation/swiftui/textinputdictationactivation)
- [TextInputDictationBehavior](https://developer.apple.com/documentation/swiftui/textinputdictationbehavior)

## Configuring the Writing Tools behavior {#Configuring-the-Writing-Tools-behavior}

- [writingToolsBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/writingtoolsbehavior(_:)) — Specifies the Writing Tools behavior for text and text input in the environment.
- [WritingToolsBehavior](https://developer.apple.com/documentation/swiftui/writingtoolsbehavior) — The Writing Tools editing experience for text and text input.
- [writingToolsAffordanceVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/writingtoolsaffordancevisibility(_:)) — Specifies whether the system should show the Writing Tools affordance for text input views affected by the environment.

## Specifying text equivalents {#Specifying-text-equivalents}

- [typeSelectEquivalent(_:)](https://developer.apple.com/documentation/swiftui/view/typeselectequivalent(_:)) — Sets an explicit type select equivalent text in a collection, such as a list or table.

## Localizing text {#Localizing-text}

- [Preparing views for localization](5.5-PreparingViewsForLocalization/) — Specify hints and add strings to localize your SwiftUI views.
- [LocalizedStringKey](https://developer.apple.com/documentation/swiftui/localizedstringkey) — The key used to look up an entry in a strings file or strings dictionary file.
- [locale](https://developer.apple.com/documentation/swiftui/environmentvalues/locale) — The current locale that views should use.
- [typesettingLanguage(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/typesettinglanguage(_:isenabled:)) — Specifies the language for typesetting.
- [TypesettingLanguage](https://developer.apple.com/documentation/swiftui/typesettinglanguage) — Defines how typesetting language is determined for text.

## Deprecated types {#Deprecated-types}

- [ContentSizeCategory](https://developer.apple.com/documentation/swiftui/contentsizecategory) — The sizes that you can specify for content.
