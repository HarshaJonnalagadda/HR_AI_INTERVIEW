import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  Avatar,
  Tab,
  Tabs,
  TextField,
  Rating,
  Divider,
  Paper,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Edit as EditIcon,
  VideoCall as VideoCallIcon,
  Phone as PhoneIcon,
  Person as PersonIcon,
  Event as EventIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';

// Mock interview data
const mockInterview = {
  id: 1,
  candidateName: 'John Doe',
  candidateId: 1,
  jobTitle: 'Senior Full Stack Developer',
  jobId: 1,
  type: 'technical',
  mode: 'video',
  date: '2024-01-22',
  time: '10:00 AM',
  duration: 60,
  status: 'scheduled',
  interviewer: 'Sarah Wilson',
  interviewerId: 1,
  location: 'Conference Room A',
  notes: 'Technical round focusing on React and Node.js',
  candidateAvatar: 'J',
  meetingLink: 'https://meet.google.com/abc-defg-hij',
  agenda: [
    'Introduction and background (10 min)',
    'Technical questions on React (20 min)',
    'Node.js and backend concepts (20 min)',
    'Q&A and next steps (10 min)',
  ],
  feedback: {
    technicalSkills: 0,
    communication: 0,
    problemSolving: 0,
    cultureFit: 0,
    overallRating: 0,
    comments: '',
    recommendation: '',
  },
  questions: [
    {
      question: 'Explain the difference between useState and useEffect hooks in React',
      answer: '',
      rating: 0,
    },
    {
      question: 'How would you optimize a slow React component?',
      answer: '',
      rating: 0,
    },
    {
      question: 'Describe your experience with Node.js and Express',
      answer: '',
      rating: 0,
    },
  ],
};

const InterviewDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [interview, setInterview] = useState(mockInterview);
  const [feedback, setFeedback] = useState(mockInterview.feedback);
  const [questions, setQuestions] = useState(mockInterview.questions);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleFeedbackChange = (field, value) => {
    setFeedback(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleQuestionUpdate = (index, field, value) => {
    setQuestions(prev => prev.map((q, i) => 
      i === index ? { ...q, [field]: value } : q
    ));
  };

  const handleSaveFeedback = () => {
    // Save feedback logic here
    console.log('Saving feedback:', feedback, questions);
  };

  const getModeIcon = (mode) => {
    switch (mode) {
      case 'video':
        return <VideoCallIcon />;
      case 'phone':
        return <PhoneIcon />;
      case 'in-person':
        return <PersonIcon />;
      default:
        return <EventIcon />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'scheduled':
        return 'primary';
      case 'completed':
        return 'success';
      case 'cancelled':
        return 'error';
      case 'rescheduled':
        return 'warning';
      default:
        return 'default';
    }
  };

  const renderTabContent = () => {
    switch (tabValue) {
      case 0:
        return (
          <Grid container spacing={3}>
            {/* Interview Details */}
            <Grid item xs={12} md={8}>
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Interview Information
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Date & Time
                    </Typography>
                    <Typography variant="body1">
                      {new Date(interview.date).toLocaleDateString()} at {interview.time}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Duration
                    </Typography>
                    <Typography variant="body1">
                      {interview.duration} minutes
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Mode
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      {getModeIcon(interview.mode)}
                      <Typography variant="body1" sx={{ ml: 1 }}>
                        {interview.mode}
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Location
                    </Typography>
                    <Typography variant="body1">
                      {interview.location}
                    </Typography>
                  </Grid>
                  {interview.meetingLink && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" color="text.secondary">
                        Meeting Link
                      </Typography>
                      <Typography variant="body1" color="primary" sx={{ cursor: 'pointer' }}>
                        {interview.meetingLink}
                      </Typography>
                    </Grid>
                  )}
                </Grid>
              </Paper>

              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Interview Agenda
                </Typography>
                <List>
                  {interview.agenda.map((item, index) => (
                    <ListItem key={index} sx={{ px: 0 }}>
                      <ListItemText
                        primary={`${index + 1}. ${item}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            {/* Candidate Info */}
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Candidate
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                    {interview.candidateAvatar}
                  </Avatar>
                  <Box>
                    <Typography variant="subtitle1" fontWeight="bold">
                      {interview.candidateName}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {interview.jobTitle}
                    </Typography>
                  </Box>
                </Box>
                <Button
                  fullWidth
                  variant="outlined"
                  onClick={() => navigate(`/candidates/${interview.candidateId}`)}
                >
                  View Profile
                </Button>
              </Paper>

              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Interviewer
                </Typography>
                <Typography variant="body1" fontWeight="medium">
                  {interview.interviewer}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Technical Lead
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Interview Questions
            </Typography>
            {questions.map((question, index) => (
              <Paper key={index} sx={{ p: 3, mb: 2 }}>
                <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                  Q{index + 1}: {question.question}
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  placeholder="Candidate's answer..."
                  value={question.answer}
                  onChange={(e) => handleQuestionUpdate(index, 'answer', e.target.value)}
                  sx={{ mb: 2 }}
                />
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Typography variant="body2">Rating:</Typography>
                  <Rating
                    value={question.rating}
                    onChange={(event, newValue) => {
                      handleQuestionUpdate(index, 'rating', newValue);
                    }}
                  />
                </Box>
              </Paper>
            ))}
          </Box>
        );

      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Interview Feedback
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Skills Assessment
                  </Typography>
                  
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="body2" gutterBottom>
                      Technical Skills
                    </Typography>
                    <Rating
                      value={feedback.technicalSkills}
                      onChange={(event, newValue) => {
                        handleFeedbackChange('technicalSkills', newValue);
                      }}
                    />
                  </Box>

                  <Box sx={{ mb: 3 }}>
                    <Typography variant="body2" gutterBottom>
                      Communication
                    </Typography>
                    <Rating
                      value={feedback.communication}
                      onChange={(event, newValue) => {
                        handleFeedbackChange('communication', newValue);
                      }}
                    />
                  </Box>

                  <Box sx={{ mb: 3 }}>
                    <Typography variant="body2" gutterBottom>
                      Problem Solving
                    </Typography>
                    <Rating
                      value={feedback.problemSolving}
                      onChange={(event, newValue) => {
                        handleFeedbackChange('problemSolving', newValue);
                      }}
                    />
                  </Box>

                  <Box sx={{ mb: 3 }}>
                    <Typography variant="body2" gutterBottom>
                      Culture Fit
                    </Typography>
                    <Rating
                      value={feedback.cultureFit}
                      onChange={(event, newValue) => {
                        handleFeedbackChange('cultureFit', newValue);
                      }}
                    />
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  <Box>
                    <Typography variant="body2" gutterBottom>
                      Overall Rating
                    </Typography>
                    <Rating
                      value={feedback.overallRating}
                      onChange={(event, newValue) => {
                        handleFeedbackChange('overallRating', newValue);
                      }}
                      size="large"
                    />
                  </Box>
                </Paper>
              </Grid>

              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3, height: 'fit-content' }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Comments & Recommendation
                  </Typography>
                  
                  <TextField
                    fullWidth
                    multiline
                    rows={6}
                    label="Detailed Comments"
                    placeholder="Provide detailed feedback about the candidate's performance..."
                    value={feedback.comments}
                    onChange={(e) => handleFeedbackChange('comments', e.target.value)}
                    sx={{ mb: 3 }}
                  />

                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    label="Recommendation"
                    placeholder="Your recommendation for next steps..."
                    value={feedback.recommendation}
                    onChange={(e) => handleFeedbackChange('recommendation', e.target.value)}
                    sx={{ mb: 3 }}
                  />

                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<SaveIcon />}
                    onClick={handleSaveFeedback}
                  >
                    Save Feedback
                  </Button>
                </Paper>
              </Grid>
            </Grid>
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/interviews')}
          sx={{ mr: 2 }}
        >
          Back to Interviews
        </Button>
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h4" fontWeight="bold">
            Interview Details
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {interview.candidateName} - {interview.jobTitle}
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<EditIcon />}
            onClick={() => navigate(`/interviews/${id}/edit`)}
          >
            Edit
          </Button>
          {interview.status === 'scheduled' && (
            <Button
              variant="outlined"
              startIcon={<CancelIcon />}
              color="error"
            >
              Cancel
            </Button>
          )}
        </Box>
      </Box>

      {/* Interview Summary Card */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={8}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <Avatar sx={{ bgcolor: 'primary.main', width: 48, height: 48 }}>
                  {interview.candidateAvatar}
                </Avatar>
                <Box>
                  <Typography variant="h6" fontWeight="bold">
                    {interview.candidateName}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {interview.jobTitle}
                  </Typography>
                </Box>
              </Box>
              
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip
                  label={interview.status}
                  color={getStatusColor(interview.status)}
                />
                <Chip
                  label={interview.type}
                  variant="outlined"
                />
                <Chip
                  label={interview.mode}
                  variant="outlined"
                />
              </Box>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: { xs: 'left', md: 'right' } }}>
                <Typography variant="h6" color="primary.main">
                  {new Date(interview.date).toLocaleDateString()}
                </Typography>
                <Typography variant="body1" fontWeight="medium">
                  {interview.time}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {interview.duration} minutes
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Details" />
            <Tab label="Questions" />
            <Tab label="Feedback" />
          </Tabs>
        </Box>
        <CardContent>
          {renderTabContent()}
        </CardContent>
      </Card>
    </Box>
  );
};

export default InterviewDetails;
