# Fitting images into available space

Adjust the size and shape of images in your app’s user interface by applying view modifiers.

## Overview {#Overview}

Image sizes vary widely, from single-pixel PNG files to digital photography images with millions of pixels. Because device sizes also vary, apps commonly need to make runtime adjustments to image sizes so they fit within the visible user interface. SwiftUI provides modifiers to scale, clip, and transform images to fit your interface perfectly.

### Scale a large image to fit its container using resizing {#Scale-a-large-image-to-fit-its-container-using-resizing}

Consider the image `Landscape_4.jpg`, a photograph with the dimensions 4032 x 3024, showing a water wheel, the surrounding building, and the sky above.

![A photo looking up at a water wheel and its surrounding building, with the sky and clouds above.](./images/SwiftUI-FIIAS-Landscape_4-original.jpg)

The following example loads the image directly into an [Image](https://developer.apple.com/documentation/swiftui/image) view, and then places it in a 300 x 400 point frame, with a blue border:

```swift
    Image("Landscape_4")
        .frame(width: 300, height: 400, alignment: .topLeading)
        .border(.blue)
```

As seen in the following screenshot, the image data loads at full size into the view, so only the clouds from the upper left of the original image are visible. Because the image renders at full size, and the blue frame is smaller than the original image, the image extends beyond the frame’s boundaries.

![An image that shows a frame with a blue border overlaid on an image of a water wheel. The image is so much larger than the available space that only a portion of the sky and clouds from the upper left of the original image is visible. The image goes beyond the borders of the outline.](./images/SwiftUI-FIIAS-unscaled@2x.png)

To fix this, you need to apply two modifiers to the `Image`:

- [resizable(capInsets:resizingMode:)](https://developer.apple.com/documentation/swiftui/image/resizable(capinsets:resizingmode:)) tells the image view to adjust the image representation to match the size of the view. By default, this modifier scales the image by reducing the size of larger images and enlarges images smaller than the view. By itself, this modifier scales each axis of the image independently.
- [aspectRatio(_:contentMode:)](https://developer.apple.com/documentation/swiftui/view/aspectratio(_:contentmode:)) corrects the behavior where the image scaling is different for each axis. This preserves the image’s original aspect ratio, using one of two strategies defined by the [ContentMode](https://developer.apple.com/documentation/swiftui/contentmode) enumeration. [ContentMode.fit](https://developer.apple.com/documentation/swiftui/contentmode/fit) scales the image to fit the view size along one axis, possibly leaving empty space along the other axis. [ContentMode.fill](https://developer.apple.com/documentation/swiftui/contentmode/fill) scales the image to fill the entire view.
```swift
  Image("Landscape_4")
      .resizable()
      .aspectRatio(contentMode: .fit)
      .frame(width: 300, height: 400, alignment: .topLeading)
      .border(.blue)
```

![An image that shows a frame with a blue border overlaid on an image of a water wheel. The water wheel image is scaled to fit the width of the containing rectangle. Empty space extends from the bottom of the image to the bottom of the rectangle.](./images/SwiftUI-FIIAS-resizeToFit@2x.png)

### Keep image data inside the view’s bounds using clipping {#Keep-image-data-inside-the-views-bounds-using-clipping}

If you use [ContentMode.fill](https://developer.apple.com/documentation/swiftui/contentmode/fill) when scaling an image, a portion of an image may extend beyond the view’s bounds, unless the view matches the image’s aspect ratio exactly. The following example illustrates this problem:

```swift
    Image("Landscape_4")
        .resizable()
        .aspectRatio(contentMode: .fill)
        .frame(width: 300, height: 400, alignment: .topLeading)
        .border(.blue)
```

![An image that shows a frame with a blue border overlaid on an image of a water wheel. The water wheel image fills its entire space vertically, and extends past the right edge of the frame horizontally.](./images/SwiftUI-FIIAS-resizeToFill-noClip@2x.png)

To prevent this problem, add the [clipped(antialiased:)](https://developer.apple.com/documentation/swiftui/view/clipped(antialiased:)) modifier. This modifier simply cuts off excess image rendering at the bounding frame of the view. Optionally, you can add an antialiasing behavior to apply smoothing to the edges of the clipping rectangle; this parameter defaults to `false`. The following example shows the effect of adding clipping to the previous fill-mode example:

```swift
    Image("Landscape_4")
        .resizable()
        .aspectRatio(contentMode: .fill)
        .frame(width: 300, height: 400, alignment: .topLeading)
        .border(.blue)
        .clipped()
```

![An image that shows a frame with a blue border overlaid on an image of a water wheel. The water wheel image fills the entire frame vertically and horizontally. The right side of the image is cut off at the right side of the rectangle.](./images/SwiftUI-FIIAS-resizeToFill-clipped@2x.png)

### Use interpolation flags to adjust rendered image quality {#Use-interpolation-flags-to-adjust-rendered-image-quality}

Rendering an image at anything other than its original size requires *interpolation*: using the existing image data to approximate a representation at a different size. Different approaches to performing interpolation have different trade-offs between computational complexity and visual quality of the rendered image. You can use the [interpolation(_:)](https://developer.apple.com/documentation/swiftui/image/interpolation(_:)) modifier to provide a hint for SwiftUI rendering behavior.

It’s easier to see the effect of interpolation when scaling a smaller image into a larger space, because the rendered image requires more image data than is available. Consider the following example, which renders a 34 x 34 image named `dot_green` into the same 300 x 400 container frame as before:

```swift
    Image("dot_green")
        .resizable()
        .interpolation(.none)
        .aspectRatio(contentMode: .fit)
        .frame(width: 300, height: 400, alignment: .topLeading)
        .border(.blue)
```

Passing the [Image.Interpolation.none](https://developer.apple.com/documentation/swiftui/image/interpolation/none) value to [interpolation(_:)](https://developer.apple.com/documentation/swiftui/image/interpolation(_:)) results in a highly pixelated rendered image.

![A green dot with a darker green border, scaled to many times its original size and highly pixelated.](./images/SwiftUI-FIIAS-smallImage-interpolation-none@2x.png)

If you change the interpolation value to [Image.Interpolation.medium](https://developer.apple.com/documentation/swiftui/image/interpolation/medium), SwiftUI smoothes out the pixel data to produce an image that isn’t as pixelated:

![A green dot with a darker green border, scaled to many times its original size, but with its edges smoothed.](./images/SwiftUI-FIIAS-smallImage-interpolation-medium@2x.png)

> Tip: You can also specify interpolation behavior when scaling images down, to ensure the highest quality image possible, fastest rendering time, or a behavior in between.

### Fill a space with a repeating image using tiling {#Fill-a-space-with-a-repeating-image-using-tiling}

When you have an image that’s much smaller than the space you want to render it into, another option  to fill the space is *tiling*: repeating the same image over and over again. To tile an image, pass the [Image.ResizingMode.tile](https://developer.apple.com/documentation/swiftui/image/resizingmode/tile) parameter to the [resizable(capInsets:resizingMode:)](https://developer.apple.com/documentation/swiftui/image/resizable(capinsets:resizingmode:)) modifier:

```swift
    Image("dot_green")
        .resizable(resizingMode: .tile)
        .frame(width: 300, height: 400, alignment: .topLeading)
        .border(.blue)
```

![A rectangular blue outline, 300 by 400. The repeated green dot image fills its entire space horizontally and vertically.](./images/SwiftUI-FIIAS-smallImage-tile@2x.png)

Tiling can be particuarly useful when using an image that, when placed end-to-end with copies of itself, creates a larger pattern with no visual discontinuities.
