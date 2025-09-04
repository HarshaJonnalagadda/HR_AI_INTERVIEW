import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Avatar,
  Chip,
  TextField,
  Paper,
  IconButton,
  LinearProgress,
  Divider,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Phone as PhoneIcon,
  PhoneDisabled as PhoneDisabledIcon,
  Mic as MicIcon,
  MicOff as MicOffIcon,
  VolumeUp as VolumeUpIcon,
  VolumeOff as VolumeOffIcon,
  Save as SaveIcon,
  Person as PersonIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';

// Mock candidate data
const mockCandidate = {
  id: 1,
  name: 'John Doe',
  email: 'john.doe@email.com',
  phone: '+91 9876543210',
  currentRole: 'Senior Developer',
  currentCompany: 'Tech Solutions',
  jobTitle: 'Senior Full Stack Developer',
  avatar: 'J',
};

const VoiceCall = () => {
  const { candidateId } = useParams();
  const navigate = useNavigate();
  const [candidate] = useState(mockCandidate);
  const [callStatus, setCallStatus] = useState('idle'); // idle, calling, connected, ended
  const [callDuration, setCallDuration] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const [isSpeakerOn, setIsSpeakerOn] = useState(false);
  const [callNotes, setCallNotes] = useState('');
  const [callStartTime, setCallStartTime] = useState(null);

  useEffect(() => {
    let interval;
    if (callStatus === 'connected' && callStartTime) {
      interval = setInterval(() => {
        setCallDuration(Math.floor((Date.now() - callStartTime) / 1000));
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [callStatus, callStartTime]);

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStartCall = async () => {
    setCallStatus('calling');
    
    // Simulate call connection
    setTimeout(() => {
      setCallStatus('connected');
      setCallStartTime(Date.now());
    }, 3000);
  };

  const handleEndCall = () => {
    setCallStatus('ended');
    setCallStartTime(null);
  };

  const handleToggleMute = () => {
    setIsMuted(!isMuted);
  };

  const handleToggleSpeaker = () => {
    setIsSpeakerOn(!isSpeakerOn);
  };

  const handleSaveNotes = () => {
    // Save call notes logic
    console.log('Saving call notes:', callNotes);
    navigate('/candidates');
  };

  const getCallStatusColor = () => {
    switch (callStatus) {
      case 'calling':
        return 'warning';
      case 'connected':
        return 'success';
      case 'ended':
        return 'error';
      default:
        return 'primary';
    }
  };

  const getCallStatusText = () => {
    switch (callStatus) {
      case 'calling':
        return 'Calling...';
      case 'connected':
        return 'Connected';
      case 'ended':
        return 'Call Ended';
      default:
        return 'Ready to Call';
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto' }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/candidates')}
          sx={{ mr: 2 }}
        >
          Back to Candidates
        </Button>
        <Typography variant="h4" fontWeight="bold">
          Voice Call
        </Typography>
      </Box>

      {/* Call Interface */}
      <Grid container spacing={3}>
        {/* Main Call Card */}
        <Grid item xs={12} md={8}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              {/* Candidate Info */}
              <Avatar
                sx={{
                  bgcolor: 'primary.main',
                  width: 120,
                  height: 120,
                  mx: 'auto',
                  mb: 2,
                  fontSize: '3rem',
                }}
              >
                {candidate.avatar}
              </Avatar>
              
              <Typography variant="h4" fontWeight="bold" gutterBottom>
                {candidate.name}
              </Typography>
              
              <Typography variant="h6" color="text.secondary" gutterBottom>
                {candidate.currentRole}
              </Typography>
              
              <Typography variant="body1" color="text.secondary" gutterBottom>
                {candidate.phone}
              </Typography>

              {/* Call Status */}
              <Box sx={{ my: 3 }}>
                <Chip
                  label={getCallStatusText()}
                  color={getCallStatusColor()}
                  size="large"
                  sx={{ fontSize: '1rem', py: 2, px: 3 }}
                />
              </Box>

              {/* Call Duration */}
              {callStatus === 'connected' && (
                <Typography variant="h5" color="success.main" gutterBottom>
                  {formatDuration(callDuration)}
                </Typography>
              )}

              {/* Calling Animation */}
              {callStatus === 'calling' && (
                <Box sx={{ my: 3 }}>
                  <LinearProgress color="warning" />
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Connecting to {candidate.name}...
                  </Typography>
                </Box>
              )}

              {/* Call Controls */}
              <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 4 }}>
                {callStatus === 'idle' && (
                  <Button
                    variant="contained"
                    size="large"
                    startIcon={<PhoneIcon />}
                    onClick={handleStartCall}
                    sx={{
                      bgcolor: 'success.main',
                      '&:hover': { bgcolor: 'success.dark' },
                      px: 4,
                      py: 1.5,
                    }}
                  >
                    Start Call
                  </Button>
                )}

                {(callStatus === 'connected' || callStatus === 'calling') && (
                  <>
                    <IconButton
                      size="large"
                      onClick={handleToggleMute}
                      sx={{
                        bgcolor: isMuted ? 'error.main' : 'action.hover',
                        color: isMuted ? 'white' : 'text.primary',
                        '&:hover': {
                          bgcolor: isMuted ? 'error.dark' : 'action.selected',
                        },
                      }}
                    >
                      {isMuted ? <MicOffIcon /> : <MicIcon />}
                    </IconButton>

                    <IconButton
                      size="large"
                      onClick={handleToggleSpeaker}
                      sx={{
                        bgcolor: isSpeakerOn ? 'primary.main' : 'action.hover',
                        color: isSpeakerOn ? 'white' : 'text.primary',
                        '&:hover': {
                          bgcolor: isSpeakerOn ? 'primary.dark' : 'action.selected',
                        },
                      }}
                    >
                      {isSpeakerOn ? <VolumeUpIcon /> : <VolumeOffIcon />}
                    </IconButton>

                    <Button
                      variant="contained"
                      size="large"
                      startIcon={<PhoneDisabledIcon />}
                      onClick={handleEndCall}
                      sx={{
                        bgcolor: 'error.main',
                        '&:hover': { bgcolor: 'error.dark' },
                        px: 4,
                        py: 1.5,
                      }}
                    >
                      End Call
                    </Button>
                  </>
                )}

                {callStatus === 'ended' && (
                  <Button
                    variant="contained"
                    size="large"
                    startIcon={<PhoneIcon />}
                    onClick={handleStartCall}
                    sx={{
                      bgcolor: 'success.main',
                      '&:hover': { bgcolor: 'success.dark' },
                      px: 4,
                      py: 1.5,
                    }}
                  >
                    Call Again
                  </Button>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Side Panel */}
        <Grid item xs={12} md={4}>
          <Grid container spacing={2}>
            {/* Candidate Details */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Candidate Details
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <PersonIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Current Role
                    </Typography>
                    <Typography variant="body1">
                      {candidate.currentRole}
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <PersonIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Company
                    </Typography>
                    <Typography variant="body1">
                      {candidate.currentCompany}
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <PersonIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Applied For
                    </Typography>
                    <Typography variant="body1">
                      {candidate.jobTitle}
                    </Typography>
                  </Box>
                </Box>

                <Button
                  fullWidth
                  variant="outlined"
                  onClick={() => navigate(`/candidates/${candidate.id}`)}
                  sx={{ mt: 2 }}
                >
                  View Full Profile
                </Button>
              </Paper>
            </Grid>

            {/* Quick Actions */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Quick Actions
                </Typography>
                
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<ScheduleIcon />}
                  onClick={() => navigate(`/interviews/schedule?candidateId=${candidate.id}`)}
                  sx={{ mb: 1 }}
                >
                  Schedule Interview
                </Button>
                
                <Button
                  fullWidth
                  variant="outlined"
                  onClick={() => window.open(`mailto:${candidate.email}`)}
                >
                  Send Email
                </Button>
              </Paper>
            </Grid>
          </Grid>
        </Grid>

        {/* Call Notes */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Call Notes
              </Typography>
              
              <TextField
                fullWidth
                multiline
                rows={6}
                placeholder="Add notes about the call, candidate responses, next steps, etc..."
                value={callNotes}
                onChange={(e) => setCallNotes(e.target.value)}
                sx={{ mb: 2 }}
              />

              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  {callStatus === 'ended' && callDuration > 0 && (
                    `Call duration: ${formatDuration(callDuration)}`
                  )}
                </Typography>
                
                <Button
                  variant="contained"
                  startIcon={<SaveIcon />}
                  onClick={handleSaveNotes}
                  disabled={!callNotes.trim()}
                >
                  Save Notes
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default VoiceCall;
