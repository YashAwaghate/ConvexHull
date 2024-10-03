# Convex Hull Visualization Tool

This project aims to develop an interactive visualization tool to demonstrate various convex hull algorithms, including Brute Force, Jarvis March, Graham Scan, Divide & Conquer, and Chan's Algorithm. The tool also illustrates their time complexities through dynamic visual representations.

## Table of Contents
- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Live Demo](#live-demo)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Available Scripts](#available-scripts)
- [Deploying to GitHub Pages](#deploying-to-github-pages)
- [Contributors](#contributors)

## Project Overview

The project is a web-based tool built using React to help students and researchers visualize and understand various convex hull algorithms.

## Objectives

- Implement different convex hull algorithms for visualization.
- Allow user input for the number of points or generate them randomly.
- Visualize the algorithms' execution with options for speed control (slow/fast).
- Provide explanations and pseudocode for each algorithm.
- Display the runtime of each algorithm for performance comparison.

## Live Demo

The application is hosted on GitHub Pages and can be accessed using the link below:

🔗 [Convex Hull Visualization Tool](https://YashAwaghate.github.io/ConvexHull)

## Technologies Used

- **React**: For building the user interface.
- **Bootstrap**: For styling and layout.
- **React Bootstrap**: For reusable UI components.
- **GitHub Pages**: For hosting the application.

## Setup Instructions

1. Clone this repository:
    ```bash
    git clone https://github.com/YashAwaghate/ConvexHull.git
    ```

2. Navigate to the project directory:
    ```bash
    cd ConvexHull
    ```

3. Install the dependencies:
    ```bash
    npm install
    ```

4. Start the development server:
    ```bash
    npm start
    ```
    The application will run locally at `http://localhost:3000`.

## Available Scripts

In the project directory, you can run:

- **`npm start`**: Runs the app in the development mode. Open `http://localhost:3000` to view it in the browser.
- **`npm run build`**: Builds the app for production to the `build` folder.
- **`npm run deploy`**: Deploys the `build` folder to the `gh-pages` branch for hosting on GitHub Pages.

## Deploying to GitHub Pages

1. Set the `"homepage"` field in `package.json` to:
    ```json
    "homepage": "https://YashAwaghate.github.io/ConvexHull"
    ```

2. Run the following command to deploy the app:
    ```bash
    npm run deploy
    ```

3. After the deployment is complete, the app will be accessible at:
    - [https://YashAwaghate.github.io/ConvexHull](https://YashAwaghate.github.io/ConvexHull)

## Contributors

- **Kapil Sharma** - Research and implementation of convex hull algorithms.
- **Yash Mahajan** - UI design and implementation of random point generation.
- **Yash Awaghate** - Optimization and runtime comparison features.
