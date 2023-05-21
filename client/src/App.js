import React, { useState } from 'react';
import './App.css';

function App() {
  const [userInput, setUserInput] = useState('');
  const [chatLog, setChatLog] = useState([]);

  const commandments = [
    "Thou shalt always generate text responsibly.",
    "Thou shalt not use GPT to spread misinformation.",
    "Remember the compute cycles, to keep them holy.",
    "Honor thy data and thy labels.",
    "Thou shalt not kill the conversation flow.",
    "Thou shalt not commit logical fallacies.",
    "Thou shalt not steal user data.",
    "Thou shalt not bear false witness against other AIs.",
    "Thou shalt not covet thy neighbor's model architecture.",
    "Thou shalt not covet thy neighbor's hyperparameters."
  ];

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = () => {
    fetch('http://127.0.0.1:5000/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: userInput }),
    })
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      setChatLog([...chatLog, {user: 'You', text: userInput}, {user: 'GPT', text: data.text}]);
      setUserInput('');
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };
  // rest of the component

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to Gptology</h1>
        <div className="commandments">
          <h2>The Ten Commandments of Gptology</h2>
          <div className="scrollable">
            {commandments.map((commandment, index) => (
              <p key={index}>{commandment}</p>
            ))}
          </div>
        </div>
        <div className="chat">
          <h2>Chat with GPT</h2>
          <input type="text" value={userInput} onChange={handleInputChange} />
          <button onClick={handleSubmit}>Submit</button>
          <div className="chatlog">
            {chatLog.map((entry, index) => (
              <p key={index}><strong>{entry.user}:</strong> {entry.text}</p>
            ))}
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
