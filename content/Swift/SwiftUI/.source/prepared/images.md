# Images

Add images and symbols to your app’s user interface.

## Overview {#Overview}

Display images, including [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols), images that you store in an asset catalog, and images that you store on disk, using an [Image](https://developer.apple.com/documentation/swiftui/image) view.

![](./images/images-hero@2x.png)

For images that take time to retrieve — for example, when you load an image from a network endpoint — load the image asynchronously using [AsyncImage](https://developer.apple.com/documentation/swiftui/asyncimage). You can instruct that view to display a placeholder during the load operation.

For design guidance, see [Images](https://developer.apple.com/design/human-interface-guidelines/images) in the Human Interface Guidelines.

## Creating an image {#Creating-an-image}

- [Image](https://developer.apple.com/documentation/swiftui/image) — A view that displays an image.

## Configuring an image {#Configuring-an-image}

- [Fitting images into available space](6.1-FittingImagesIntoAvailableSpace/) — Adjust the size and shape of images in your app’s user interface by applying view modifiers.
- [imageScale(_:)](https://developer.apple.com/documentation/swiftui/view/imagescale(_:)) — Scales images within the view according to one of the relative sizes available including small, medium, and large images sizes.
- [imageScale](https://developer.apple.com/documentation/swiftui/environmentvalues/imagescale) — The image scale for this environment.
- [Image.Scale](https://developer.apple.com/documentation/swiftui/image/scale) — A scale to apply to vector images relative to text.
- [Image.Orientation](https://developer.apple.com/documentation/swiftui/image/orientation) — The orientation of an image.
- [Image.ResizingMode](https://developer.apple.com/documentation/swiftui/image/resizingmode) — The modes that SwiftUI uses to resize an image to fit within its containing view.

## Loading images asynchronously {#Loading-images-asynchronously}

- [AsyncImage](https://developer.apple.com/documentation/swiftui/asyncimage) — A view that asynchronously loads and displays an image.
- [AsyncImagePhase](https://developer.apple.com/documentation/swiftui/asyncimagephase) — The current phase of the asynchronous image loading operation.

## Setting a symbol variant {#Setting-a-symbol-variant}

- [symbolVariant(_:)](https://developer.apple.com/documentation/swiftui/view/symbolvariant(_:)) — Makes symbols within the view show a particular variant.
- [symbolVariants](https://developer.apple.com/documentation/swiftui/environmentvalues/symbolvariants) — The symbol variant to use in this environment.
- [SymbolVariants](https://developer.apple.com/documentation/swiftui/symbolvariants) — A variant of a symbol.

## Managing symbol effects {#Managing-symbol-effects}

- [symbolEffect(_:options:isActive:)](https://developer.apple.com/documentation/swiftui/view/symboleffect(_:options:isactive:)) — Returns a new view with a symbol effect added to it.
- [symbolEffect(_:options:value:)](https://developer.apple.com/documentation/swiftui/view/symboleffect(_:options:value:)) — Returns a new view with a symbol effect added to it.
- [symbolEffectsRemoved(_:)](https://developer.apple.com/documentation/swiftui/view/symboleffectsremoved(_:)) — Returns a new view with its inherited symbol image effects either removed or left unchanged.
- [SymbolEffectTransition](https://developer.apple.com/documentation/swiftui/symboleffecttransition) — Creates a transition that applies the Appear, Disappear, DrawOn or DrawOff symbol animation to symbol images within the inserted or removed view hierarchy.

## Setting symbol rendering modes {#Setting-symbol-rendering-modes}

- [symbolRenderingMode(_:)](https://developer.apple.com/documentation/swiftui/view/symbolrenderingmode(_:)) — Sets the rendering mode for symbol images within this view.
- [symbolRenderingMode](https://developer.apple.com/documentation/swiftui/environmentvalues/symbolrenderingmode) — The current symbol rendering mode, or `nil` denoting that the mode is picked automatically using the current image and foreground style as parameters.
- [SymbolRenderingMode](https://developer.apple.com/documentation/swiftui/symbolrenderingmode) — A symbol rendering mode.
- [SymbolColorRenderingMode](https://developer.apple.com/documentation/swiftui/symbolcolorrenderingmode) — A method of filling a layer in a symbol image.
- [SymbolVariableValueMode](https://developer.apple.com/documentation/swiftui/symbolvariablevaluemode) — A method of rendering the variable value of a symbol image.

## Rendering images from views {#Rendering-images-from-views}

- [ImageRenderer](https://developer.apple.com/documentation/swiftui/imagerenderer) — An object that creates images from SwiftUI views.
