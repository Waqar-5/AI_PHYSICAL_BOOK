# Unity Environment Building Example

This example demonstrates a very basic interaction within a Unity environment: rotating an object. This serves as a fundamental building block for creating more complex environments and behaviors in Unity.

## Prerequisites

1.  **Unity Hub and Unity Editor**: Ensure you have Unity Hub installed and at least one version of the Unity Editor (e.g., 2022.3.x LTS) installed.
2.  **Basic Unity Project**: You should have an existing Unity 3D project. If not, create a new 3D project in Unity Hub.

## How to Use

1.  **Open your Unity Project**: Launch your Unity Editor and open the 3D project where you want to add this example.
2.  **Create a 3D Object**: In your Unity Scene, create any 3D object that you want to rotate. For instance:
    *   Right-click in the Hierarchy window.
    *   Select `3D Object` -> `Cube` (or `Sphere`, `Cylinder`, etc.).
3.  **Create a C# Script File**:
    *   In the Project window (Assets folder), right-click.
    *   Select `Create` -> `C# Script`.
    *   Name the script exactly `RotateObject` (it must match the class name in the `.cs` file).
4.  **Copy the Script Content**:
    *   Open the newly created `RotateObject.cs` file in your code editor.
    *   Copy the content from `example_unity_environment.cs` into this new `RotateObject.cs` file, overwriting its default content. Save the file.
5.  **Attach the Script to the Object**:
    *   Drag the `RotateObject` script from your Project window onto the 3D object (e.g., the Cube) in your Hierarchy window.
    *   Alternatively, select the 3D object in the Hierarchy, then in the Inspector window, click `Add Component` and search for `RotateObject`.
6.  **Adjust Rotation Speed (Optional)**:
    *   With the 3D object still selected in the Hierarchy, look at the Inspector window. You should see the `Rotate Object` component.
    *   You can adjust the `Rotation Speed` property directly in the Inspector.
7.  **Run the Scene**:
    *   Click the `Play` button in the Unity Editor to run your scene.
    *   You should observe your 3D object rotating around its Y-axis.

## Script Functionality

The `RotateObject.cs` script is a simple MonoBehaviour that makes the GameObject it is attached to rotate continuously around its local Y-axis.

*   `rotationSpeed`: A public variable that allows you to control the speed of rotation directly from the Unity Editor's Inspector window.
*   `Update()`: This method is called once per frame. Inside `Update`, `transform.Rotate(0, rotationSpeed * Time.deltaTime, 0)` rotates the GameObject. `Time.deltaTime` is used to ensure the rotation speed is frame-rate independent.

This example illustrates how simple C# scripting can add dynamic behavior to objects in your Unity environment, a foundational step for building interactive digital twins.