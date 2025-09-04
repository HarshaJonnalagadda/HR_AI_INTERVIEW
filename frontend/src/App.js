import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout/Layout';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import Dashboard from './pages/Dashboard/Dashboard';
import Jobs from './pages/Jobs/Jobs';
import JobDetails from './pages/Jobs/JobDetails';
import CreateJob from './pages/Jobs/CreateJob';
import Candidates from './pages/Candidates/Candidates';
import CandidateDetails from './pages/Candidates/CandidateDetails';
import Interviews from './pages/Interviews/Interviews';
import InterviewDetails from './pages/Interviews/InterviewDetails';
import VoiceCall from './pages/VoiceCall/VoiceCall';
import ProtectedRoute from './components/Auth/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected Routes */}
          <Route path="/" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            
            {/* Jobs Routes */}
            <Route path="jobs" element={<Jobs />} />
            <Route path="jobs/create" element={<CreateJob />} />
            <Route path="jobs/:id" element={<JobDetails />} />
            
            {/* Candidates Routes */}
            <Route path="candidates" element={<Candidates />} />
            <Route path="candidates/:id" element={<CandidateDetails />} />
            
            {/* Interviews Routes */}
            <Route path="interviews" element={<Interviews />} />
            <Route path="interviews/:id" element={<InterviewDetails />} />
            
            {/* Voice Call Route */}
            <Route path="voice-call/:candidateId" element={<VoiceCall />} />
          </Route>
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Box>
    </AuthProvider>
  );
}

export default App;
