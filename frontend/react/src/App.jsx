
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header.jsx';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import MyContests from './pages/MyContests.jsx';
import CreateContest from './pages/CreateContest.jsx';
import Home from './pages/Home.jsx';
import EditContest from './pages/EditContest.jsx';
import EditQuizField from './pages/EditQuizField.jsx';
import EditContestants from './pages/EditContestants.jsx';
import EditSubmissions from './pages/EditSubmissions.jsx';
import SolveContest from './pages/SolveContest.jsx';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/my-contests" element={<MyContests />} />
          <Route path="/create-contest" element={<CreateContest />} />
          <Route path="/edit-contest/:contestId" element={<EditContest />} />
          <Route path="/edit-field" element={<EditQuizField />} />
          <Route path="/edit-contestants" element={<EditContestants />} />
          <Route path="/edit-submissions" element={<EditSubmissions />} />
          <Route path="/contest" element={<SolveContest />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
