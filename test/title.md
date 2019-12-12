## Building for Fuchsia
Escher itself is part of any Fuchsia build that includes Scenic, i.e. any build that targets a device with a screen.  The Escher examples and tests are built by adding `//garnet/packages/examples:escher` and `//garnet/packages/tests:escher` to your `fx set` invocation.
