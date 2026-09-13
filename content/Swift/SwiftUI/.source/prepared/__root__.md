# SwiftUI

Declare the user interface and behavior for your app on every platform.

## Overview {#Overview}

SwiftUI provides views, controls, and layout structures for declaring your app’s user interface. The framework provides event handlers for delivering taps, gestures, and other types of input to your app, and tools to manage the flow of data from your app’s models down to the views and controls that users see and interact with.

Define your app structure using the [App](https://developer.apple.com/documentation/swiftui/app) protocol, and populate it with scenes that contain the views that make up your app’s user interface. Create your own custom views that conform to the [View](https://developer.apple.com/documentation/swiftui/view) protocol, and compose them with SwiftUI views for displaying text, images, and custom shapes using stacks, lists, and more. Apply powerful modifiers to built-in views and your own views to customize their rendering and interactivity. Share code between apps on multiple platforms with views and controls that adapt to their context and presentation.

![An image of the Landmarks sample app on Mac, iPad, and iPhone showing the Mount Fuji landmark.](./images/landmarks-app-article-hero@2x.png)

You can integrate SwiftUI views with objects from the [UIKit](https://developer.apple.com/documentation/uikit), [AppKit](https://developer.apple.com/documentation/appkit), and [WatchKit](https://developer.apple.com/documentation/watchkit) frameworks to take further advantage of platform-specific functionality. You can also customize accessibility support in SwiftUI, and localize your app’s interface for different languages, countries, or cultural regions.

> Tip: If you’re new to SwiftUI, visit the [SwiftUI Pathway](https://developer.apple.com/swiftui/get-started/). It’s a collection of tutorials, articles, and sample projects that help you get started with SwiftUI.

### Featured samples {#Featured-samples}

- [Landmarks: Building an app with Liquid Glass](essentials/1-LandmarksBuildingAnAppWithLiquidGlass/)
- [Wishlist: Planning travel in a SwiftUI app](views/1-ViewFundamentals/1.2-WishlistPlanningTravelInASwiftuiApp/)
- [Destination Video](https://developer.apple.com/documentation/visionos/destination-video)
- [Building a document-based app with SwiftUI](appstructure/5-Documents/5.4-BuildingADocumentBasedAppWithSwiftui/)

## Essentials {#Essentials}

- [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) — Find out how to bring the new material to your app.
- [Develop in Swift](https://developer.apple.com/tutorials/develop-in-swift) — Develop in Swift Tutorials introduce app development with Swift and Xcode to anyone learning to build apps for Apple platforms.
- [SwiftUI updates](https://developer.apple.com/documentation/updates/swiftui) — Learn about important changes to SwiftUI.
- [Landmarks: Building an app with Liquid Glass](essentials/1-LandmarksBuildingAnAppWithLiquidGlass/) — Enhance your app experience with system-provided and custom Liquid Glass.

## App structure {#App-structure}

- [App organization](appstructure/1-AppOrganization/) — Define the entry point and top-level structure of your app.
- [Scenes](appstructure/2-Scenes/) — Declare the user interface groupings that make up the parts of your app.
- [Windows](appstructure/3-Windows/) — Display user interface content in a window or a collection of windows.
- [Immersive spaces](appstructure/4-ImmersiveSpaces/) — Display unbounded content in a person’s surroundings.
- [Documents](appstructure/5-Documents/) — Enable people to open and manage documents.
- [Navigation](appstructure/6-Navigation/) — Enable people to move between different parts of your app’s view hierarchy within a scene.
- [Modal presentations](appstructure/7-ModalPresentations/) — Present content in a separate view that offers focused interaction.
- [Toolbars](appstructure/8-Toolbars/) — Provide immediate access to frequently used commands and controls.
- [Search](appstructure/9-Search/) — Enable people to search for text or other content within your app.
- [App extensions](appstructure/10-AppExtensions/) — Extend your app’s basic functionality to other parts of the system, like by adding a Widget.

## Data and storage {#Data-and-storage}

- [Model data](datastorage/1-ModelData/) — Manage the data that your app uses to drive its interface.
- [Environment values](datastorage/2-EnvironmentValues/) — Share data throughout a view hierarchy using the environment.
- [Preferences](datastorage/3-Preferences/) — Indicate configuration preferences from views to their container views.
- [Persistent storage](datastorage/4-PersistentStorage/) — Store data for use across sessions of your app.

## Views {#Views}

- [View fundamentals](views/1-ViewFundamentals/) — Define the visual elements of your app using a hierarchy of views.
- [View configuration](views/2-ViewConfiguration/) — Adjust the characteristics of views in a hierarchy.
- [View styles](views/3-ViewStyles/) — Apply built-in and custom appearances and behaviors to different types of views.
- [Animations](views/4-Animations/) — Create smooth visual updates in response to state changes.
- [Text input and output](views/5-TextInputAndOutput/) — Display formatted text and get text input from the user.
- [Images](views/6-Images/) — Add images and symbols to your app’s user interface.
- [Controls and indicators](views/7-ControlsAndIndicators/) — Display values and get user selections.
- [Menus and commands](views/8-MenusAndCommands/) — Provide space-efficient, context-dependent access to commands and controls.
- [Shapes](views/9-Shapes/) — Trace and fill built-in and custom shapes with a color, gradient, or other pattern.
- [Drawing and graphics](views/10-DrawingAndGraphics/) — Enhance your views with graphical effects and customized drawings.

## View layout {#View-layout}

- [Layout fundamentals](viewlayout/1-LayoutFundamentals/) — Arrange views inside built-in layout containers like stacks and grids.
- [Layout adjustments](viewlayout/2-LayoutAdjustments/) — Make fine adjustments to alignment, spacing, padding, and other layout parameters.
- [Custom layout](viewlayout/3-CustomLayout/) — Place views in custom arrangements and create animated transitions between layout types.
- [Lists](viewlayout/4-Lists/) — Display a structured, scrollable column of information.
- [Tables](viewlayout/5-Tables/) — Display selectable, sortable data arranged in rows and columns.
- [View groupings](viewlayout/6-ViewGroupings/) — Present views in different kinds of purpose-driven containers, like forms or control groups.
- [Scroll views](viewlayout/7-ScrollViews/) — Enable people to scroll to content that doesn’t fit in the current display.

## Event handling {#Event-handling}

- [Gestures](eventhandling/1-Gestures/) — Define interactions from taps, clicks, and swipes to fine-grained gestures.
- [Input events](eventhandling/2-InputEvents/) — Respond to input from a hardware device, like a keyboard or a Touch Bar.
- [Clipboard](eventhandling/3-Clipboard/) — Enable people to move or duplicate items by issuing Copy and Paste commands.
- [Drag and drop](eventhandling/4-DragAndDrop/) — Enable people to move or duplicate items by dragging them from one location to another.
- [Focus](eventhandling/5-Focus/) — Identify and control which visible object responds to user interaction.
- [System events](eventhandling/6-SystemEvents/) — React to system events, like opening a URL.

## Accessibility {#Accessibility}

- [Accessibility fundamentals](accessibility/1-AccessibilityFundamentals/) — Make your SwiftUI apps accessible to everyone, including people with disabilities.
- [Accessible appearance](accessibility/2-AccessibleAppearance/) — Enhance the legibility of content in your app’s interface.
- [Accessible controls](accessibility/3-AccessibleControls/) — Improve access to actions that your app can undertake.
- [Accessible descriptions](accessibility/4-AccessibleDescriptions/) — Describe interface elements to help people understand what they represent.
- [Accessible navigation](accessibility/5-AccessibleNavigation/) — Enable users to navigate to specific user interface elements using rotors.

## Framework integration {#Framework-integration}

- [AppKit integration](frameworkintegration/1-AppkitIntegration/) — Add AppKit views to your SwiftUI app, or use SwiftUI views in your AppKit app.
- [UIKit integration](frameworkintegration/2-UikitIntegration/) — Add UIKit views to your SwiftUI app, or use SwiftUI views in your UIKit app.
- [WatchKit integration](frameworkintegration/3-WatchkitIntegration/) — Add WatchKit views to your SwiftUI app, or use SwiftUI views in your WatchKit app.
- [Technology-specific views](frameworkintegration/4-TechnologySpecificViews/) — Use SwiftUI views that other Apple frameworks provide.

## Tool support {#Tool-support}

- [Previews in Xcode](views/1.3-PreviewsInXcode/) — Generate dynamic, interactive previews of your custom views.
- [Xcode library customization](toolsupport/1-XcodeLibraryCustomization/) — Expose custom views and modifiers in the Xcode library.
- [Performance analysis](toolsupport/2-PerformanceAnalysis/) — Measure and improve your app’s responsiveness.
