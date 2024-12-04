import { TextareaAutosize } from '@mui/material'
import React from 'react'

const styles={
    paddingBottom: '10px'
}

const UserInput = ({ setPayload }) => {
  const [value, setValue] = React.useState("");

  const handleOnChange = (event) => {
    const newValue = event.target.value;
    setValue(newValue);

    const convertedText = convertTextToArray(newValue);
    console.log("Converted Text to Array:", convertedText);
    setPayload(convertedText);
  };

  function convertTextToArray(text) {

    const lines = text.trim().split("\n");


    const result = lines.map((line) =>
      line.trim().split(/\s+/).map(Number)
    );

    return result;
  }

  return (
    <div style={styles}>
      <TextareaAutosize value={value} onChange={handleOnChange} />
    </div>
  );
};


export default UserInput