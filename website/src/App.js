import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    term: '',
    phone_number: '',
    carrier: '',
    class_nums: []
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleClassNumsChange = (e, index) => {
    const { value } = e.target;
    setFormData(prevState => {
      const updatedClassNums = [...prevState.class_nums];
      updatedClassNums[index] = value;
      return {
        ...prevState,
        class_nums: updatedClassNums
      };
    });
  };

  const handleAddClassNum = () => {
    setFormData(prevState => ({
      ...prevState,
      class_nums: [...prevState.class_nums, '']
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you can make your POST request with formData
    console.log(formData)
    fetch('http://52.40.67.97/waitlist-notification/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
      // Handle response
      console.log(data);
    })
    .catch(error => {
      // Handle error
      console.error('Error:', error);
    });
  };

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text" name="username" value={formData.username} onChange={handleChange} />
        </label>
        <br />
        <label>
          Password:
          <input type="password" name="password" value={formData.password} onChange={handleChange} />
        </label>
        <br />
        <label>
          Term:
          <input type="text" name="term" value={formData.term} onChange={handleChange} />
        </label>
        <br />
        <label>
          Phone Number:
          <input type="text" name="phone_number" value={formData.phone_number} onChange={handleChange} />
        </label>
        <br />
        <label>
          Carrier:
          <input type="text" name="carrier" value={formData.carrier} onChange={handleChange} />
        </label>
        <br />
        <label>
          Class Numbers:
          {formData.class_nums.map((classNum, index) => (
            <div key={index}>
              <input
                type="text"
                value={classNum}
                onChange={(e) => handleClassNumsChange(e, index)}
              />
            </div>
          ))}
          <button type="button" onClick={handleAddClassNum}>Add Class Number</button>
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default App;
