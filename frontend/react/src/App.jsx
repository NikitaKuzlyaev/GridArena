
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header.jsx';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import MyContests from './pages/MyContests.jsx';
import CreateContest from './pages/CreateContest.jsx';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<h1>Hello World</h1>} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/my-contests" element={<MyContests />} />
          <Route path="/create-contest" element={<CreateContest />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
