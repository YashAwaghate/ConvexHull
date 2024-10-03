// src/App.js
import React from 'react';
import './App.css';

const ReportSection = ({ title, content }) => {
  return (
    <div className="section">
      <h2>{title}</h2>
      {content}
    </div>
  );
};

const App = () => {
  return (
    <div className="container">
      <h1>Convex Hull Visualization Tool</h1>
      <h3>Kapil Sharma (ks4643), Yash Mahajan (ym9800), Yash Awaghate (ya2390)</h3>

      <ReportSection
        title="1. Description"
        content={
          <>
            <p>
              This project aims to develop an interactive visualization tool to demonstrate various convex hull algorithms, including Brute Force, Jarvis March, Graham Scan, Divide & Conquer, and Chan's Algorithm. The tool will also illustrate their time complexities through dynamic visual representations.
            </p>
            <h4>Objectives:</h4>
            <ul>
              <li>Implement different convex hull algorithms for visualization.</li>
              <li>Allow user input for the number of points or generate them randomly.</li>
              <li>Visualize the algorithms' execution with options for speed control (slow/fast).</li>
              <li>Provide a small explanation and pseudocode for each algorithm.</li>
              <li>Display the runtime of each algorithm in seconds for comparison.</li>
              <li>Enhance educational understanding by visualizing algorithmic steps and complexities.</li>
            </ul>
          </>
        }
      />

      <ReportSection
        title="2. Timeline"
        content={
          <table className="timeline">
            <thead>
              <tr>
                <th>Week</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Week 1</td>
                <td>Finalize convex hull algorithms to be implemented. Research and design UI wireframes.</td>
              </tr>
              <tr>
                <td>Week 2</td>
                <td>Set up the basic structure of the web app and create initial visualization for point generation (random/user-defined).</td>
              </tr>
              <tr>
                <td>Week 3</td>
                <td>Implement and visualize the Brute Force convex hull algorithm.</td>
              </tr>
              <tr>
                <td>Week 4</td>
                <td>Implement and visualize Jarvis March algorithm. Add explanatory content and pseudocode for the algorithms.</td>
              </tr>
              <tr>
                <td>Week 5</td>
                <td>Implement Graham Scan algorithm and add functionality to compare runtimes for different algorithms.</td>
              </tr>
              <tr>
                <td>Week 6</td>
                <td>Implement Divide & Conquer algorithm. Integrate speed control (slow/fast) for visualization.</td>
              </tr>
              <tr>
                <td>Week 7</td>
                <td>Implement Chan's Algorithm and add user options for runtime comparisons with varying numbers of points.</td>
              </tr>
              <tr>
                <td>Week 8</td>
                <td>Optimize the tool, test edge cases, finalize UI, and gather user feedback. Write documentation and prepare the final report.</td>
              </tr>
            </tbody>
          </table>
        }
      />

      <ReportSection
        title="3. References"
        content={
          <ul>
            <li><a href="https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API">WebGL API Documentation</a></li>
            <li><a href="https://webglfundamentals.org/">WebGL Fundamentals</a></li>
            <li>Computational Geometry: Algorithms and Applications, 3rd ed., Springer.</li>
            <li><a href="https://gsap.com/docs/v3/GSAP/">GSAP Animation Library</a></li>
            <li><a href="https://www.chartjs.org/docs/latest/">Chart.js Documentation</a></li>
            <li><a href="https://d3js.org/getting-started">D3.js Getting Started</a></li>
          </ul>
        }
      />

      <ReportSection
        title="4. Work Division"
        content={
          <>
            <h4>Kapil Sharma:</h4>
            <ul>
              <li>Finalize the list of convex hull algorithms and research their time complexities.</li>
              <li>Create the React app and set up the initial project structure.</li>
              <li>Implement the Jarvis March algorithm and assist with adding explanatory content and pseudocode.</li>
              <li>Assist with testing edge cases and provide feedback for the optimization of the tool.</li>
              <li>Contribute to writing the final documentation and report.</li>
            </ul>

            <h4>Yash Mahajan:</h4>
            <ul>
              <li>Design UI wireframes and research methods to visualize algorithms dynamically.</li>
              <li>Implement random point generation and user input functionality for the number of points.</li>
              <li>Implement Divide & Conquer and Chan's algorithms.</li>
              <li>Handle speed control functionality for visualizations (slow/fast mode).</li>
              <li>Assist in optimizing the tool, finalize the UI, and contribute to documentation.</li>
            </ul>

            <h4>Yash Awaghate:</h4>
            <ul>
              <li>Implement the Brute Force and Graham Scan algorithms.</li>
              <li>Integrate runtime comparison features and ensure each algorithm displays its runtime in seconds.</li>
              <li>Research techniques for step-by-step visualization and user interaction.</li>
              <li>Lead the final optimization, testing, and user feedback gathering processes.</li>
              <li>Oversee the preparation of the final documentation and ensure all features are well-documented.</li>
            </ul>
          </>
        }
      />
    </div>
  );
};

export default App;
