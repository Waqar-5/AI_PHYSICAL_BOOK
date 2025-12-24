# Chapter 2: Unity Environment Building and Interactions

## Introduction to Unity as a Digital Twin Platform

Unity is a powerful cross-platform game engine that is increasingly used beyond gaming, including for robotics simulation and digital twin applications. Its strong visual rendering capabilities, physics engine (separate from Gazebo, but can be synchronized), and extensive asset store make it an excellent choice for creating rich, interactive, and visually appealing digital environments. In a digital twin context, Unity can serve as the high-fidelity visualization and interaction layer, often working in conjunction with a robotics middleware like ROS 2 or dedicated physics simulators like Gazebo.

## Key Concepts for Environment Building

### Scenes and GameObjects
*   **Scene**: A Unity scene acts as a container for your digital twin environment. It holds all the GameObjects that make up the scene, such as terrain, robots, sensors, lights, cameras, and UI elements. Each scene can represent a different environment or a different state of an environment.
*   **GameObject**: The fundamental object in Unity. Everything in a scene is a GameObject, including models, cameras, and scripts. GameObjects have a `Transform` component (position, rotation, scale) by default and can have many other components attached to them to define their behavior and appearance.

### Components
Components are the building blocks of GameObjects. They define the functionality of a GameObject.
*   **Mesh Filter & Mesh Renderer**: Together, these display 3D models. The Mesh Filter holds the mesh data (geometry), and the Mesh Renderer renders it using materials.
*   **Collider**: Defines the physical shape of a GameObject for collision detection. Can be primitive shapes (Box Collider, Sphere Collider, Capsule Collider) or custom Mesh Colliders.
*   **Rigidbody**: Adds physics properties to a GameObject, allowing it to be influenced by gravity and forces, and to interact with other physics-enabled objects.
*   **Light**: Components that emit light into the scene.
*   **Camera**: Defines what part of the scene is rendered to the display.

### Asset Management
Unity's asset pipeline makes it easy to import and manage various types of assets:
*   **3D Models**: Import models (e.g., FBX, OBJ, GLTF) for robots, objects, and environment elements.
*   **Materials and Textures**: Define the visual properties (color, shininess, texture) of 3D models.
*   **Scripts**: C# scripts are used to define custom behaviors and logic for GameObjects.
*   **Prefabs**: Reusable GameObjects that can be instantiated multiple times in a scene. Essential for creating complex environments efficiently (e.g., multiple robots, identical furniture).

## Building a Digital Twin Environment in Unity

1.  **Project Setup**: Create a new Unity 3D project.
2.  **Import Assets**: Import 3D models (e.g., from CAD, Blender, or Unity Asset Store) for your robot, environment, and any interactive elements.
3.  **Scene Design**:
    *   **Terrain**: Create or import terrain to represent the ground.
    *   **Place GameObjects**: Drag and drop imported models into the scene as GameObjects. Position, rotate, and scale them using the Transform component.
    *   **Lighting**: Add directional lights, point lights, or spot lights to illuminate the scene realistically.
    *   **Cameras**: Place cameras to provide different views of the environment (e.g., a fixed camera, a third-person camera following the robot).
4.  **Add Physics**:
    *   Attach `Rigidbody` components to GameObjects that need to interact physically (e.g., the robot, movable objects).
    *   Attach `Collider` components to all GameObjects that should participate in collision detection. Ensure collision layers are set up correctly to manage interactions.
5.  **Scripting for Interactions**:
    *   Write C# scripts to define robot control logic (if Unity is controlling the robot), user interaction (e.g., moving objects with a mouse), or environmental changes.
    *   Scripts can respond to input events, physics events (collisions), and communicate with external systems (e.g., ROS 2 via Unity-ROS packages, or custom network protocols).

## Basic Human-Robot Interaction (HRI) in Unity

Unity is well-suited for HRI visualization and interaction:
*   **UI Elements**: Use Unity's UI system (Canvas, UI elements like buttons, sliders, text) to create dashboards, control panels, or display robot status.
*   **Input Handling**: Capture user input from keyboard, mouse, or game controllers to control a simulated robot or interact with the environment.
*   **Visualization**: Visualize robot states (e.g., joint angles, end-effector position), sensor data (e.g., LiDAR scans, camera feeds from simulated cameras), or mission progress directly within the 3D environment.
*   **Teleoperation**: Implement teleoperation interfaces where a human user can control the simulated robot in real-time.

## Basic Human-Robot Interaction (HRI) in Unity

Unity is well-suited for HRI visualization and interaction:
*   **UI Elements**: Use Unity's UI system (Canvas, UI elements like buttons, sliders, text) to create dashboards, control panels, or display robot status.
*   **Input Handling**: Capture user input from keyboard, mouse, or game controllers to control a simulated robot or interact with the environment.
*   **Visualization**: Visualize robot states (e.g., joint angles, end-effector position), sensor data (e.g., LiDAR scans, camera feeds from simulated cameras), or mission progress directly within the 3D environment.
*   **Teleoperation**: Implement teleoperation interfaces where a human user can control the simulated robot in real-time.

## Code Example: Unity Environment Interaction

This example demonstrates a basic Unity script to rotate an object, illustrating how C# scripting can add dynamic behavior to objects in your Unity environment.

For the full code and detailed setup instructions, refer to the [example_unity_environment.cs](https://github.com/your_repo/blob/main/examples/module2/environment_building/example_unity_environment.cs) and its [README.md](https://github.com/your_repo/blob/main/examples/module2/environment_building/README.md) in the project repository.

### `example_unity_environment.cs`

```csharp
using UnityEngine;

public class RotateObject : MonoBehaviour
{
    public float rotationSpeed = 50f; // Speed of rotation in degrees per second

    // Update is called once per frame
    void Update()
    {
        // Rotate the GameObject around its Y-axis
        transform.Rotate(0, rotationSpeed * Time.deltaTime, 0);
    }
}
```

### Setup and Running the Example

```markdown
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
```

## Script Functionality

The `RotateObject.cs` script is a simple MonoBehaviour that makes the GameObject it is attached to rotate continuously around its local Y-axis.

*   `rotationSpeed`: A public variable that allows you to control the speed of rotation directly from the Unity Editor's Inspector window.
*   `Update()`: This method is called once per frame. Inside `Update`, `transform.Rotate(0, rotationSpeed * Time.deltaTime, 0)` rotates the GameObject. `Time.deltaTime` is used to ensure the rotation speed is frame-rate independent.

This example illustrates how simple C# scripting can add dynamic behavior to objects in your Unity environment, a foundational step for building interactive digital twins.

## Small Task: Implement Player Control for an Object

**Objective**: Modify the Unity example to allow a player to move a 3D object using keyboard input (e.g., arrow keys or WASD).

1.  **Create a new C# script**: Name it `PlayerControl.cs`.
2.  **Attach the script**: Attach this new script to a 3D object in your scene (e.g., a Cube).
3.  **Implement movement**: In the `Update` method of `PlayerControl.cs`, use `Input.GetAxis("Horizontal")` and `Input.GetAxis("Vertical")` to get horizontal and vertical input. Apply this input to the object's `transform.position` to move it.
4.  **Test**: Run the Unity scene and verify that you can control the object's movement with the keyboard.

## Conclusion

Unity offers a rich environment for building visually compelling and interactive digital twin environments. By mastering its concepts of GameObjects, Components, and scripting, you can create sophisticated simulations for robotics. When combined with dedicated physics engines like Gazebo (or Unity's own physics engine) and communication frameworks like ROS 2, Unity becomes a powerful tool for developing, testing, and visualizing complex robotic systems. The next chapter will delve into how to simulate various sensors to perceive these environments.