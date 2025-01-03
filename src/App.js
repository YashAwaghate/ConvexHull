import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import UserInput from './UserInput';

const ReportSection = ({ title, content }) => {
  return (
    <div className="section">
      <h2>{title}</h2>
      {content}
    </div>
  );
};

const AlgorithmSection = ({ title, description, pseudocode, runAlgorithm, isLoading, currentAlgorithm }) => {
  return (
    <div className="algorithm-section">
      <h3>{title}</h3>
      <p>{description}</p>
      <h4>Pseudocode:</h4>
      <pre className="pseudocode">{pseudocode}</pre>
      <button onClick={runAlgorithm} disabled={isLoading} style={{ marginTop: '10px' }}>
        {isLoading && currentAlgorithm === title.toLowerCase().replace(' ', '') ? `Running ${title}...` : `Run ${title}`}
      </button>
    </div>
  );
};

const App = () => {
  const [algorithmOutput, setAlgorithmOutput] = useState(''); // State for the output
  const [isLoading, setIsLoading] = useState(false); // State to show a loading indicator
  const [currentAlgorithm, setCurrentAlgorithm] = useState(''); // To track which algorithm is running
  const [payload, setPayload] = useState([]);
  const [numPoints, setNumPoints] = useState(10); // Number of points to generate

  const runAlgorithm = async (algorithmName) => {
    setIsLoading(true)
    setAlgorithmOutput(false);
    setCurrentAlgorithm(algorithmName);
    try {
      const response = await axios.post(`https://convex-hull-backend.vercel.app/run-${algorithmName}`, {
        payload,
        numPoints,
      });
      setAlgorithmOutput(response.data);
    } catch (error) {
      console.error(`Error running ${algorithmName}:`, error);
      setAlgorithmOutput(`An error occurred while running ${algorithmName}.`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container" style={{ margin: '0', padding: '0', width: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header Section */}
      <div className="header" style={{ padding: '20px', backgroundColor: '#2c3e50', color: 'white', textAlign: 'center' }}>
        <h1>Convex Hull Visualization</h1>
        <p>An interactive tool to visualize and understand various convex hull algorithms.</p>
      </div>

      <div className="main-content" style={{ display: 'flex', flex: '1' }}>
        {/* Left panel for all the sections */}
        <div
          className="left-panel"
          style={{
            flex: '3',
            padding: '20px',
            overflowY: 'auto',
            borderRight: '1px solid #ddd',
          }}
        >
          {/* Description Section */}
          <ReportSection
            title="1. Description"
            content={
              <>
                <p>
                  This project aims to develop an interactive visualization tool to demonstrate various convex hull
                  algorithms, including Brute Force, Jarvis March, Graham Scan, Divide & Conquer, and Chan's Algorithm.
                  The tool will also illustrate their time complexities through dynamic visual representations.
                </p>
                <a href='https://drive.google.com/file/d/1MrtqRdVBRH2WFoA5eWA8-aeSepJpQMwT/view?pli=1' target="_blank">Link to our final presentation</a>
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

          {/* Algorithm Implementations */}
          <ReportSection
            title="2. Implementations"
            content={
              <>
                <AlgorithmSection
                  title="Brute Force"
                  description="The Brute Force algorithm iterates through all possible pairs of points to determine which points form the convex hull. It has a high time complexity but is conceptually simple."
                  pseudocode={`
for each pair of points (p1, p2):
  find line formed by p1 and p2
  check if all other points are on the same side of the line
  if yes, add (p1, p2) to the hull
                  `}
                  runAlgorithm={() => runAlgorithm('bruteforce')}
                  isLoading={isLoading}
                  currentAlgorithm={currentAlgorithm}
                />

                <AlgorithmSection
                  title="Divide & Conquer"
                  description="The Divide & Conquer algorithm splits the set of points into smaller subsets, finds the convex hull for each subset, and then merges them together."
                  pseudocode={`
divide the set of points into two halves
recursively find the convex hull of each half
merge the two convex hulls to get the final result
                  `}
                  runAlgorithm={() => runAlgorithm('divide')}
                  isLoading={isLoading}
                  currentAlgorithm={currentAlgorithm}
                />

                <AlgorithmSection
                  title="Graham Scan"
                  description="The Graham Scan algorithm sorts points based on polar angles with respect to the lowest point and then constructs the hull using a stack."
                  pseudocode={`
sort points by polar angle with respect to a reference point
initialize an empty stack
for each point:
  while the top of the stack is not a left turn, pop it
  push the current point onto the stack
                  `}
                  runAlgorithm={() => runAlgorithm('graham')}
                  isLoading={isLoading}
                  currentAlgorithm={currentAlgorithm}
                />

                <AlgorithmSection
                  title="Jarvis March"
                  description="Jarvis March, also known as the Gift Wrapping algorithm, finds the convex hull by repeatedly selecting the leftmost point until returning to the starting point."
                  pseudocode={`
start with the leftmost point
repeat until you return to the starting point:
  select the point with the smallest polar angle with respect to the current point
  add it to the hull
                  `}
                  runAlgorithm={() => runAlgorithm('jarvis')}
                  isLoading={isLoading}
                  currentAlgorithm={currentAlgorithm}
                />

                <AlgorithmSection
                  title="Monotone Chain"
                  description="The Monotone Chain algorithm sorts the points and constructs the lower and upper hulls independently, combining them to get the convex hull."
                  pseudocode={`
sort the points by x-coordinate
construct the lower hull by iterating from left to right
construct the upper hull by iterating from right to left
combine the lower and upper hulls
                  `}
                  runAlgorithm={() => runAlgorithm('monotone')}
                  isLoading={isLoading}
                  currentAlgorithm={currentAlgorithm}
                />
              </>
            }
          />

          {/* Timeline Section */}
          <ReportSection
            title="3. Timeline"
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
                    <td>Research and finalize the convex hull algorithms to be implemented. Start designing the app.</td>
                  </tr>
                  <tr>
                    <td>Week 2</td>
                    <td>Set up the basic structure of the web app and establish the backend.</td>
                  </tr>
                  <tr>
                    <td>Week 3</td>
                    <td>Implement and visualize the Brute Force convex hull algorithm.</td>
                  </tr>
                  <tr>
                    <td>Week 4</td>
                    <td>Implement and visualize the Jarvis March algorithm. Add pseudocode and explanatory content for Brute Force and Jarvis March algorithms.</td>
                  </tr>
                  <tr>
                    <td>Week 5</td>
                    <td>Implement Graham Scan algorithm.</td>
                  </tr>
                  <tr>
                    <td>Week 6</td>
                    <td>Implement Divide & Conquer algorithm.</td>
                  </tr>
                  <tr>
                    <td>Week 7</td>
                    <td>Implement Monotone Algorithm and research ways to integrate visualizations effectively.</td>
                  </tr>
                  <tr>
                    <td>Week 8</td>
                    <td>Implement Chan's Algorithm.</td>
                  </tr>
                  <tr>
                    <td>Week 9</td>
                    <td>Create initial visualization tools for point generation (random/user-defined). Begin integration testing and refine all algorithms.</td>
                  </tr>
                  <tr>
                    <td>Week 10</td>
                    <td>Integrate speed control (slow/fast) for visualizations. Optimize visualization performance.</td>
                  </tr>
                  <tr>
                    <td>Week 11</td>
                    <td>Complete backend deployment and frontend integration testing.</td>
                  </tr>
                  <tr>
                    <td>Week 12</td>
                    <td>Finalize UI/UX design, gather user feedback, and polish user experience.</td>
                  </tr>
                  <tr>
                    <td>Week 13</td>
                    <td>Write final documentation, prepare presentation materials, and wrap up the project.</td>
                  </tr>
                </tbody>
              </table>
            }
          />

          {/* References Section */}
          <ReportSection
            title="4. References"
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

          {/* Work Division Section */}
          <ReportSection
            title="5. Work Division"
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

        {/* Right panel for output */}
        <div
          className="right-panel"
          style={{
            flex: '2',
            padding: '20px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'flex-start',
            position: 'sticky',
            top: '20px',
            height: '100vh',
            borderLeft: '1px solid #ddd',
          }}
        >
          <h2>Output</h2>
          <UserInput setPayload={setPayload} />
          <div style={{ marginBottom: '20px', width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <label htmlFor="numPoints" style={{ marginBottom: '5px' }}>Number of Random Points:</label>
            <input
              type="number"
              id="numPoints"
              value={numPoints}
              onChange={(e) => setNumPoints(e.target.value)}
              min="1"
              style={{ width: '60px' }}
            />
          </div>
          {!algorithmOutput && <p style={{ marginTop: '20px' }}>Run an algorithm to see the output here...</p>}
          {algorithmOutput&&(
            <ReportSection
              title={`${currentAlgorithm.charAt(0).toUpperCase() + currentAlgorithm.slice(1)} Algorithm Output`}
              content={
                <div style={{ width: '100%' }}>
                  <img
                    src={algorithmOutput}
                    alt="Base64 Image"
                    style={{
                      width: '100%',
                      maxWidth: '100%',
                      height: 'auto',
                      border: '1px solid #ddd',
                      borderRadius: '8px',
                    }}
                  />
                </div>
              }
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
