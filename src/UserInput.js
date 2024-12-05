import { TextareaAutosize } from '@mui/material';
import React from 'react';

const styles = {
  paddingBottom: '10px',
};

const UserInput = ({ setPayload }) => {
  const [value, setValue] = React.useState('');

  const handleOnChange = (event) => {
    const newValue = event.target.value;
    setValue(newValue);

    const convertedText = convertTextToArray(newValue);
    setPayload(convertedText);
  };

  const handleBlur = () => {
    if (!value.trim()) {
      setValue(''); // Reset to keep placeholder if no input is entered
    }
  };

  function convertTextToArray(text) {
    const lines = text.trim().split('\n');
    return lines.map((line) => line.trim().split(/\s+/).map(Number));
  }

  return (
    <div style={styles}>
      <p style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '5px' }}>
        Input Format: x and y coordinates space-separated, new line for each point.
      </p>
      <TextareaAutosize
        value={value}
        onChange={handleOnChange}
        onBlur={handleBlur} // Ensure placeholder reappears if no input is entered
        placeholder="Insert input here"
        minRows={2} // Adjusted for smaller height
        maxRows={4} // Limit maximum expansion
        style={{
          width: '100%',
          padding: '10px',
          fontSize: '1rem',
          backgroundColor: '#2d313a',
          color: '#fff',
          border: '1px solid #444',
          borderRadius: '5px',
          outline: 'none',
        }}
      />
    </div>
  );
};

export default UserInput;
