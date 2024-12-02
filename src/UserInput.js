import { TextareaAutosize } from '@mui/material'
import React from 'react'

const styles={
    paddingBottom: '10px'
}

const UserInput = ({setPayload})=>{ 

    const[value, setValue] = React.useState("")

    const handleOnChange=(event)=>{
        setValue(event.target.value)
        const convertedText = convertTextToArray(value)
        console.log(convertedText)
        setPayload(convertedText)
    }

    function convertTextToArray(text) {
        // Split the text by lines
        const lines = text.trim().split("\n");
      
        // Convert each line into an array of numbers
        const result = lines.map(line => 
          line.split(" ").map(Number)
        );
      
        return result;
      }

    return(
        <div style={styles}>
           <TextareaAutosize value={value} onChange={handleOnChange}/>
        </div>
    )
}

export default UserInput