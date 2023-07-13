Assignment 2 - Cow Rollercoaster

The objective of this assignment was to create an animation featuring a cow that follows a Catmull-Rom spline passing through six user-selected points.

1) SimpleScene.py:

- Some necessary imports were added to the code, such as the math module, to ensure certain mathematical functions are available.

- Several variables were introduced to store and track various data within the program. These include savedCount, initialCow, savedLoc, startTime, timeInitialized, and rollerCow.

- A new class called PickInfo was implemented. This class likely contains specific information related to picking or selecting objects in the program.

- Additional functions were defined to perform various operations within the code. These functions include handling vectors, positions, rotations, and transformations, as well as extracting translation information from matrices. Additionally, there are functions for creating planes, handling key press events, drawing camera views, frames, cows, and the floor. Lastly, there are functions for calculating parameters and derivatives related to Bezier curves and determining cow directions.

- Some variables present in the original code were removed.

- The reshape function was modified to adjust the viewport and perspective projection to match the desired display configuration.

- The initialize function was updated to include additional initialization steps. These steps involve setting up camera models, loading the cow model, and configuring the floor texture.

- The loadModel() function was modified to adjust the scale and position of the cow model, ensuring it is displayed correctly within the scene.

- The motion function underwent changes to handle the rotation and translation of the cow model. These modifications enable user interaction with the cow object, allowing it to be moved and rotated.

- The scroll function was modified to handle zooming in and out of the cow model. This change provides the user with the ability to control the zoom level for a more detailed or broader view of the cow.


- The edited code has improved the readability and style of the code by following some Python conventions, such as using snake_case for variable names, adding spaces around operators and commas, and removing unused or redundant variables.


- The edited code does have handle features of the OBJ format, such as parameter space vertices, line elements, smoothing groups, or materials.


- The edited code does use shaders or lighting effects to render the OBJ model. It enhances the appearance of the model by using modern OpenGL features such as VBOs, VAOs, shaders, uniforms, etc.


--------------------------------------------------------------------------------------

