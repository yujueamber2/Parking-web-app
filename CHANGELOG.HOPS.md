# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.16.19] - 2025-01-27

### Added

- It is now possible for Rhino.Compute to create a headless document to be used during the solve routine. To use this feature, create a local environment variable called RHINO_COMPUTE_CREATE_HEADLESS_DOC.The value of this variable can be set to either true or false with false being the default. Each time the GrasshopperSolveHelper method of the ResthopperEndpointsModule is invoked, it checks whether Config.CreateHeadlessDoc is set to true. If it is, a brand new headless document is instantiated with tolerances and units determined by the input object. This feature is useful for third party plugins which may make calls to the Rhino Document to retrieve properties such as tolerances or units. Prior to this feature, these requests would result in an error. Now, a plugin may utilize this information for calculations.

## [0.16.18] - 2025-01-06

### Fixed

- Fixed a bug where custom endpoints which pointed to functions which did not contain an argument would result in a duplicate. When this endpoint would be called, the duplicate would cause an AmbiguousMatchException to be thrown.
- Changed the `RollForward` value in both the Rhino.Compute and Compute.Geometry csproj files to use `Major` instead of `LatestMinor`. This change means that these projects will use .NET 7 if the framework is installed, but if not it will roll forward to .NET 8 or 9 (which ever is the latest major version installed on the machine). Read more at https://learn.microsoft.com/en-us/dotnet/core/versions/selection.

## [0.16.17] - 2024-11-19

### Fixed

- Startup.cs now loads the Commands.rhp so that certain features such as the gltf exporter will work properly inside rhino.compute. This is a temporary solution until the gltf exporter code is moved into Rhinocommon or Rhino.UI.

## [0.16.16] - 2024-11-07

### Fixed

- Fixed a bug where the /launch endpoint would return a NullReference exception.
- Added a line to the ComputeChildren.cs to clear the startInfo environmentVariable for "ASPNETCORE_HOSTINGSTARTUPASSEMBLIES" when Rhino.Compute starts up the child process Compute.Geometry. This was causing issues while debugging in newer version of Visual Studio.
- Fixed a bug where the ComputeRecursionLevel property was not always being set.

## [0.16.15] - 2024-11-07

### Fixed

- Fixed a bug where system directory paths were not being parsed correctly as a command line argument.

## [0.16.14] - 2024-10-30

### Fixed

- Minor bug fixes. Fixed a bug where the open file icon shown in the Set Definition dialog was blurry.

## [0.16.13] - 2024-08-29

### Fixed

- Fixed a bug in the Function Source Manager which was causing the document to expire incorrectly when multiple functions were instantiated by the Hops component.

## [0.16.12] - 2024-08-28

### Fixed

- In the change made to version 0.16.11, the schema of the default input values were changed to a DataTree<ResthopperObject>. However, this change broke some code in instances where people would be sending the older style of values as defaults. The changes made in this build (0.16.12) will now properly handle the deserialization of values sent either as a DataTree<ResthopperObject> or as the older style of default values.

## [0.16.11] - 2024-08-20

### Fixed

- Fixed an issue with default values. Previously, default values would only work on some parameter types and only if a single value was set via persistent data. Now, any parameter type (except for model objects) will work as setting a default value and you can pass in an item, list, or data tree as your default value.

### Added

- Added the ability to make some parameters act as Optional inputs. If you use a Context Get component and set the AtLeast value to 0, then that parameter will be treated as an Optional input.

## [0.16.10] - 2024-08-08

### Fixed

- Adding a fix to enfoce the localization culture of Compute.Geometry to use the CultureInfo("en-US"). This should hopefully fix some issues where users from various countries have trouble with strings converting to numbers because of comma and/or decimal separators.

## [0.16.9] - 2024-07-03

### Fixed

- Fixed a bug where setting the environment variable RHINO_COMPUTE_DEBUG to True would not in effect add any additional logging information to the console output. The default for this is True when running in debug mode, and False when running Rhino.Compute in release mode. Override this setting by creating an environment variable called RHINO_COMPUTE_DEBUG and setting the value to True or False. Note, this change will only work when targeting builds of Rhino >= 8.10.

## [0.16.8] - 2024-06-05

### Fixed

- The Rhino.Inside.Resolver was set to automatically look for the latest build of Rhino which was causing some conflicts if users had installed Rhino 9 WIP. The default path for the 8.x build of rhino.compute should now look for that latest build of Rhino 8 when trying to resolve Rhino.Inside.

### Added

- A few additional lines of logging information were added to display the the current build of Rhino.Compute and Rhino as well as the working system path.

## [0.16.7] - 2024-04-22

### Added

- Added the RhinoCompute.cs file to the compute.geometry 8.x repo. This is referenced in several guides and tutorials and had been omitted during the refactoring process when we moved from 7.x to 8.x. In addition, a new endpoint was added called `/sdk/csharp` which will allow you to view and/or download the contents of this file for use in your own projects.

## [0.16.6] - 2024-03-15

### Fixed

- Fixing another bug to handle how the RhinoCode scripting plugin is loaded in Rhino.Compute. This plugin is now loaded first before Grasshopper or other compute related plugins.

## [0.16.5] - 2024-02-29

### Fixed

- Calling the /sdk endpoint in Rhino.Compute would not return anything. This has now been fixed and it will now return a full list of all SDK methods available in Rhino.Compute.
- Fixed the module_update_compute.ps1 powershell script which can be run to update existing production environments to the latest version of Rhino.Compute.
- Fixed a bug where the RhinoCode scripting plugin was not being loaded properly in Rhino.Compute.
- Added some parameters to the launch settings to be able to debug Rhino.Compute in .NET 4.8.

## [0.16.4] - 2023-11-27

### Added

- Added support for the Box as a data type returned from rhino.compute.

## [0.16.3] - 2023-11-17

### Added

- Added a support in rhino.compute for the new Get Plane context component available in Rhino 8.

## [0.16.2] - 2023-08-23

### Added

- Added support for Rectangle3d as a data type returned from rhino.compute.

### Fixed

- Rhino.Compute and Compute.Geometry now target the .NET 7 Framework. This makes compute now compatible with Rhino 8.
- Fixed many minor bugs.

## [0.16.1] - 2023-03-23

### Added

- Two endpoints to return information about the plugins installed on the machine running the rhino.compute server.
    - /plugins/rhino/installed - will return a sorted dictionary of Rhino plugins which are installed.
    - /plugins/gh/installed - will return a sorted dictionary of Grasshopper plugins which are installed.

### Fixed

- Compute would not return the correct minimum and maximum value for the Context Get Integer component if a slider was connected as the default value.
- Compute would not return the correct default value for the Context Get Boolean if a boolean toggle was connected as the default value.
- Fixed a bug which prevented the minimum and maximum values to be set on a Contextual Number/Integer parameter if a number slider was used to define the default value. Now, the minimum and maximum value of the slider should be used for that input parameter.
- Fixed a rather serious bug which prevented the data structure from the output of the Hops component to match the same data structure returned from running native Grasshopper components. This fix should ensure that the data structures returned from Hops are consistent with examples which do not use Hops but contain the same underlying components. [See this thread for more information](https://discourse.mcneel.com/t/hops-output-tree-mismatch/155361).
- If a user set the At Least to something > 0 (ie. list access), the Hops component wouldn't detect the number of incoming items and would throw an error.

## [0.15.4] - 2022-11-23

### Fixed

- Fixing release bug to properly bundle all necessary dependencies into a self-contained exectuable

## [0.15.3] - 2022-11-05

### Fixed

- A bug where warnings were always being produced with input set to list access

## [0.15.2] - 2022-10-26

### Added

- An environment variable called `RHINO_COMPUTE_MAX_REQUEST_SIZE` can now be set to configure the maximum allowed size of any HTTP request body in bytes. The default value is set to 52428800 bytes (approx. 50mb).

## [0.15.1] - 2022-08-04

### Added

- A textbox was added to the Hops App Settings dialog (under Preferences/Solver) which allows you to set the timeout (in seconds) for the HTTP client that Hops uses to send/receive data to/from the rhino.compute server. The default is 100s but for long running calculations you may need to increase this value.

## [0.15.0] - 2022-06-10

### Added

- Hops can now internalize it's referenced definition if it is saved on a local file system. Similar to internalizing geometry, when you internalize a definition it means that it removes the reference to the external file and instead serializes the definition inside the Hops component. This means that once a referenced file is internalized, you no longer have to share the accompanying referenced definition along with the Hops file.

## [0.14.1] - 2022-05-26

### Fixed

- A bug was fixed which caused an error when parsing the numeric minimum and maximum values on the Get Number or Get Integer components.

## [0.14.0] - 2022-05-19

### Added

- DataTrees are now supported in Rhino builds >= 7.19.22130.15001 and 8.0.22131.04306. All of the contextual getter components now have a menu item which lets you set whether you want that parameter to have DataTree access. When set to true, this setting will override the AtMost value which is what Hops uses for item or list access. The DataTree access setting has no effect on the GH Player command. 
- The function manager is now available in Rhino for mac on builds >= 7.19.22126.15001 and 8.0.22126.04306. See the update below for hops build 0.13.1 for more information about how the function manager works.
- The bootstrap script which is used when deploying Rhino.Compute for a production environment has been update to follow a two-step installation process (with a restart in between). The installation is largely the same, however a restart is now required to finish the installation of the IIS modules.

### Fixed

- A bug was fixed if the Hops referenced file was not found. Now, if the referenced file is at least in the same folder as the Hops definition then it should find and load it upon opening the file.
- An error would occur when exporting last HTTP request and/or response if more than one hops component was being used in a definition.
- The Minimum and Maximum values on the contextual Get Number and Get Integer components are now used in Hops. If either of those values are set on the getter parameter and the input value exceeds that limit, an error will be thrown in Hops. 

## [0.13.1] - 2022-04-13

### Added

- A function manager was added to the Hops preferenced UI. This interface allows you to add function sources (ie. local folder, localhost, and remote server locations). Once a valid source is added to the Hops preferences, a new menu item will be added to the Hops component. This menu item will enumerate valid functions (either grasshopper files or function endpoints). Right-clicking on a menu item will open the file while left-clicking will reference the file in the Hops component (ie. like setting the path). For  now, this feature is only available when running Grasshopper for Windows.

### Fixed

- A bug was fixed which prevented the rhino.compute server from launching on local machines which had the checkbox turned on for loading .gha assemblies using COFF byte arrays in the Grasshopper developer settings.

## [0.12.0] - 2022-03-10

### Added

- The current document units (ie. feet, inches, millimeters, etc.) are now included as part of the API request from Hops.
- The Hops component now displays an error message if:
    - one or more inputs have the same name
    - one or more outputs have the same name
    - rhino.compute is missing a component. This would likely be caused if rhino.compute is running on a remote server and it is missing a 3rd party plugin.
- An environment variable called `RHINO_COMPUTE_TIMEOUT` can now be set to configure the request timeout (in seconds) for the HttpClient in the reverse proxy module.
- The bootstrap script (for deployment to production environments) has been updated to handle the installation of 3rd party plugins. The script will now create a new local user account, called `RhinoComputeUser` and auto-generate a unique password. It will add this user to the RDP group and assign this identity to the RhinoComputeAppPool which is what IIS uses to run rhino.compute.exe. The script will print the username and password at the end for your records. To install 3rd party plugins after the bootstrap script has been run, follow these steps:
    1. Log into your VM using these credentials (write these down)
        - User Name: RhinoComputeUser
        - Password: #This will be some unique password generated by the bootstrap script
    1. Install plugins using the Rhino package manager or
    1. Copy/paste plugin files to C:\Users\RhinoComputeUser\AppData\Roaming\Grasshopper\Libraries
    1. Restart the VM

### Fixed

- A bug was fixed preventing Hops from running properly in Rhino 8 WIP.

## [0.11.1] - 2022-02-08

### Fixed

- A small fix was made to the rhino.compute project to change how child processes (ie. compute.geometry) get spawn whenever the rhino.compute.exe is launched. This change was made because of how a production environment handles http requests, but this change also effected how Hops is launched from Grasshopper. Rhino.compute.exe now has a command line option called --spawn-on-startup whose default value is false. If you include this argument when you launch rhino.compute.exe then it will automatically launch a child process on startup.

## [0.11.0] - 2022-01-25

### Added

- You can now export the last API request/response made from the Hops component to the compute server. There are two endpoints that are hit during any Hops routine. In the first API call, Hops sends a request to '/io' which uploads the referenced grasshopper file to the server. Compute processes the file and returns a response with necessary information to populate the inputs and outputs on the Hops component. The Hops component gets this information and builds the inputs and outputs. It then determines what values to pass in as the input values to the definition and sends that information over to the '/solve' endpoint. Compute checks its cache to grab the right grasshopper definition and then feeds in these new input values to the definition. Once it gets a result it send it back to the Hops component which then feeds it out to the appropriate output parameter. Each of these requests and responses can now be exports (.json) so that the process can be inspected and debugged.
- An API Key input was added under the Hops preferences section. The API key is a string of text that is secret to your compute server and your applications that are using the compute API e.g. b8f91f04-3782-4f1c-87ac-8682f865bf1b. It is optional if you are testing locally, but should be used in a production environment. It is basically how the compute server ensures that the API calls are coming from your apps only. You can enter any string that is unique and secret to you and your compute apps. Make sure to keep this in a safe place.

### Fixed

- Logging was cleaned up in the compute console window. Lines that are generated from the compute.geometry project are prefixed with the letters "CG", otherwise you can assume the line was generated from the rhino.compute project. Port numbers (ie. 6001, 6002, etc.) for child processes are now also added to the compute.geometry lines as soon as they are assigned so it is easier to see which child process is handling a given request.

## [0.10.1] - 2021-11-17

### Added

- Hops output parameters can now be created using either the Context Print or Context Bake components. The nickname for these components will be used as the name of the output parameter in Hops. Note: All names should be unique (ie. no duplicates).

### Fixed

- A bug was fixed where output parameters did not retain the connection to their recipient parameters when saved/reopened.

## [0.9.0] - 2021-11-08

### Added

- Document tolerances (ie. absolute distance and angle tolerances) are now passed to rhino.compute as part of the JSON request.
- Get Boolean and Get File components are now correctly interpretted by Hops.

### Fixed

- Hops input and output parameters are now ordered based on the Y-canvas-position of the Get Components in the referenced definition.
- The maximum request body size was increased to from approximately 28.6mb to 50mb.

## [0.8.0] - 2021-08-31

### Added

- Export python sample added to Hops component context menu
- Export JSON added to Hops component context menu

### Fixed

- Default values for "Get" components can be resolved when relays are in between the component and upstream data
- Custom icons for hops components are always resized to 24x24

## [0.7.0] - 2021-06-23

### Added

- Nested hops calls now permitted with a recursion limit of 10. This limit can be modified by changing a GH app setting
- Components in named RH_OUT groups are now supported

### Fixed

- String inputs/outputs were not getting unescaped when passed back and forth between hops and compute
- Points, lines, circles were not getting converted to geometry when input to a "Get Geometry" component
- Improved error messages by forwarding errors from remote solved components
- 0.7.2: attempt to fix handling different forms of input strings in compute
- 0.7.3: handle exception in a plug-in's DocumentAdded event handler and allow request to continue

## [0.6.0] - 2021-05-30

### Added

- Path input (optional)
- Enabled input (optional)
- Asynchronous solving. Components can solve without blocking GH user interface. Asynchronous operation mode is optional per component.
- Maximum concurrent request setting to preferences

### Fixed

- Hid some preference controls on Mac that are only meant for Windows
- Component attempts to detect when inputs/outputs on a server have changed and will rebuild itself
- Removed parallel computing and variable parameters context menu items as they were unnecessary
- [0.6.2] Planes were not supported as a data type to be passed between processes

## [0.5.0] - 2021-05-18

### Added

- rhino.compute.exe now shipping with Hops on Windows and acts as a top level reverse proxy server to solve definitions.
- tree input support for python servers

### Fixed

- data output params are now passed back to hops

## [0.3.3] - 2021-03-03
## [0.1.0] - 2021-02-10
