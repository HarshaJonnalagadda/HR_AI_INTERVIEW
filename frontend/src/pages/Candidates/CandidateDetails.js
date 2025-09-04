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
  List,
  ListItem,
  ListItemText,
  Divider,
  Paper,
  LinearProgress,
} from '@mui/material';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
} from '@mui/lab';
import {
  ArrowBack as ArrowBackIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  Schedule as ScheduleIcon,
  Download as DownloadIcon,
  Star as StarIcon,
  LocationOn as LocationIcon,
  Work as WorkIcon,
  School as SchoolIcon,
  Event as EventIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';

// Mock candidate data
const mockCandidate = {
  id: 1,
  name: 'John Doe',
  email: 'john.doe@email.com',
  phone: '+91 9431937998',
  location: 'Bangalore, India',
  experience: '6 years',
  currentRole: 'Senior Developer',
  currentCompany: 'Tech Solutions',
  skills: ['React', 'Node.js', 'MongoDB', 'JavaScript', 'AWS', 'Docker', 'TypeScript', 'GraphQL'],
  status: 'active',
  stage: 'interview',
  jobTitle: 'Senior Full Stack Developer',
  rating: 4.5,
  appliedDate: '2024-01-15',
  avatar: 'J',
  summary: 'Experienced full-stack developer with 6+ years in building scalable web applications. Strong expertise in React, Node.js, and cloud technologies. Proven track record of leading development teams and delivering high-quality software solutions.',
  experience_details: [
    {
      company: 'Tech Solutions',
      role: 'Senior Developer',
      duration: '2022 - Present',
      description: 'Leading a team of 4 developers, architecting scalable solutions, and mentoring junior developers.',
    },
    {
      company: 'Digital Innovations',
      role: 'Full Stack Developer',
      duration: '2020 - 2022',
      description: 'Developed and maintained multiple client projects using React, Node.js, and MongoDB.',
    },
    {
      company: 'StartupXYZ',
      role: 'Frontend Developer',
      duration: '2018 - 2020',
      description: 'Built responsive web applications and collaborated with design teams to implement UI/UX.',
    },
  ],
  education: [
    {
      degree: 'B.Tech in Computer Science',
      institution: 'Indian Institute of Technology',
      year: '2018',
      grade: '8.5 CGPA',
    },
  ],
  timeline: [
    {
      date: '2024-01-15',
      event: 'Application Submitted',
      description: 'Candidate applied for Senior Full Stack Developer position',
      type: 'application',
    },
    {
      date: '2024-01-16',
      event: 'Resume Screened',
      description: 'Initial resume screening completed - Passed',
      type: 'screening',
    },
    {
      date: '2024-01-18',
      event: 'Phone Screening',
      description: 'Technical phone screening conducted - Positive feedback',
      type: 'call',
    },
    {
      date: '2024-01-20',
      event: 'Technical Interview Scheduled',
      description: 'Technical interview scheduled for Jan 22, 2024',
      type: 'interview',
    },
  ],
  assessments: [
    {
      name: 'Technical Assessment',
      score: 85,
      maxScore: 100,
      status: 'completed',
      date: '2024-01-17',
    },
    {
      name: 'Coding Challenge',
      score: 92,
      maxScore: 100,
      status: 'completed',
      date: '2024-01-18',
    },
    {
      name: 'System Design',
      score: 0,
      maxScore: 100,
      status: 'pending',
      date: null,
    },
  ],
};

const CandidateDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const candidate = mockCandidate; // In real app, fetch by id

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const getTimelineIcon = (type) => {
    switch (type) {
      case 'application':
        return <WorkIcon />;
      case 'screening':
        return <AssessmentIcon />;
      case 'call':
        return <PhoneIcon />;
      case 'interview':
        return <EventIcon />;
      default:
        return <EventIcon />;
    }
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<StarIcon key={i} sx={{ fontSize: 20, color: 'gold' }} />);
    }
    
    if (hasHalfStar) {
      stars.push(<StarIcon key="half" sx={{ fontSize: 20, color: 'gold', opacity: 0.5 }} />);
    }
    
    return stars;
  };

  const renderTabContent = () => {
    switch (tabValue) {
      case 0:
        return (
          <Grid container spacing={3}>
            {/* Summary */}
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Professional Summary
                </Typography>
                <Typography variant="body1" paragraph>
                  {candidate.summary}
                </Typography>
              </Paper>
            </Grid>

            {/* Experience */}
            <Grid item xs={12} md={8}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Work Experience
                </Typography>
                <List>
                  {candidate.experience_details.map((exp, index) => (
                    <React.Fragment key={index}>
                      <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                        <ListItemText
                          primary={
                            <Box>
                              <Typography variant="subtitle1" fontWeight="bold">
                                {exp.role}
                              </Typography>
                              <Typography variant="body2" color="primary">
                                {exp.company}
                              </Typography>
                            </Box>
                          }
                          secondary={
                            <Box sx={{ mt: 1 }}>
                              <Typography variant="caption" color="text.secondary">
                                {exp.duration}
                              </Typography>
                              <Typography variant="body2" sx={{ mt: 0.5 }}>
                                {exp.description}
                              </Typography>
                            </Box>
                          }
                        />
                      </ListItem>
                      {index < candidate.experience_details.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </Paper>
            </Grid>

            {/* Education & Skills */}
            <Grid item xs={12} md={4}>
              <Grid container spacing={2}>
                {/* Education */}
                <Grid item xs={12}>
                  <Paper sx={{ p: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Education
                    </Typography>
                    {candidate.education.map((edu, index) => (
                      <Box key={index}>
                        <Typography variant="subtitle2" fontWeight="bold">
                          {edu.degree}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {edu.institution}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {edu.year} • {edu.grade}
                        </Typography>
                      </Box>
                    ))}
                  </Paper>
                </Grid>

                {/* Skills */}
                <Grid item xs={12}>
                  <Paper sx={{ p: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Skills
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {candidate.skills.map((skill, index) => (
                        <Chip
                          key={index}
                          label={skill}
                          variant="outlined"
                          color="primary"
                          size="small"
                        />
                      ))}
                    </Box>
                  </Paper>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Application Timeline
            </Typography>
            <Timeline>
              {candidate.timeline.map((item, index) => (
                <TimelineItem key={index}>
                  <TimelineSeparator>
                    <TimelineDot color="primary">
                      {getTimelineIcon(item.type)}
                    </TimelineDot>
                    {index < candidate.timeline.length - 1 && <TimelineConnector />}
                  </TimelineSeparator>
                  <TimelineContent>
                    <Typography variant="subtitle2" fontWeight="bold">
                      {item.event}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {item.description}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(item.date).toLocaleDateString()}
                    </Typography>
                  </TimelineContent>
                </TimelineItem>
              ))}
            </Timeline>
          </Box>
        );

      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Assessments & Scores
            </Typography>
            <Grid container spacing={3}>
              {candidate.assessments.map((assessment, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Paper sx={{ p: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Typography variant="subtitle1" fontWeight="bold">
                        {assessment.name}
                      </Typography>
                      <Chip
                        label={assessment.status}
                        color={assessment.status === 'completed' ? 'success' : 'warning'}
                        size="small"
                      />
                    </Box>
                    
                    {assessment.status === 'completed' ? (
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Score</Typography>
                          <Typography variant="body2" fontWeight="bold">
                            {assessment.score}/{assessment.maxScore}
                          </Typography>
                        </Box>
                        <LinearProgress
                          variant="determinate"
                          value={(assessment.score / assessment.maxScore) * 100}
                          sx={{ mb: 1 }}
                        />
                        <Typography variant="caption" color="text.secondary">
                          Completed on {new Date(assessment.date).toLocaleDateString()}
                        </Typography>
                      </Box>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        Assessment pending
                      </Typography>
                    )}
                  </Paper>
                </Grid>
              ))}
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
          onClick={() => navigate('/candidates')}
          sx={{ mr: 2 }}
        >
          Back to Candidates
        </Button>
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h4" fontWeight="bold">
            {candidate.name}
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Applied for {candidate.jobTitle}
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<PhoneIcon />}
            onClick={() => navigate(`/voice-call/${candidate.id}`)}
          >
            Call
          </Button>
          <Button
            variant="outlined"
            startIcon={<ScheduleIcon />}
            onClick={() => navigate(`/interviews/schedule?candidateId=${candidate.id}`)}
          >
            Schedule
          </Button>
          <Button
            variant="contained"
            startIcon={<EmailIcon />}
          >
            Contact
          </Button>
        </Box>
      </Box>

      {/* Candidate Summary Card */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={3}>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
                <Avatar sx={{ bgcolor: 'primary.main', width: 80, height: 80, mb: 2, fontSize: '2rem' }}>
                  {candidate.avatar}
                </Avatar>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  {renderStars(candidate.rating)}
                  <Typography variant="body2" sx={{ ml: 1 }}>
                    ({candidate.rating})
                  </Typography>
                </Box>
                <Typography variant="h6" fontWeight="bold">
                  {candidate.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {candidate.currentRole}
                </Typography>
              </Box>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <EmailIcon sx={{ mr: 2, color: 'text.secondary' }} />
                  <Typography variant="body1">{candidate.email}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <PhoneIcon sx={{ mr: 2, color: 'text.secondary' }} />
                  <Typography variant="body1">{candidate.phone}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <LocationIcon sx={{ mr: 2, color: 'text.secondary' }} />
                  <Typography variant="body1">{candidate.location}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <WorkIcon sx={{ mr: 2, color: 'text.secondary' }} />
                  <Typography variant="body1">
                    {candidate.currentCompany} • {candidate.experience}
                  </Typography>
                </Box>
              </Box>
            </Grid>
            
            <Grid item xs={12} md={3}>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Status
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                    <Chip label={candidate.status} color="success" size="small" />
                    <Chip label={candidate.stage} color="primary" variant="outlined" size="small" />
                  </Box>
                </Box>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Applied Date
                  </Typography>
                  <Typography variant="body2">
                    {new Date(candidate.appliedDate).toLocaleDateString()}
                  </Typography>
                </Box>
                <Button
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  size="small"
                  fullWidth
                >
                  Download Resume
                </Button>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Profile" />
            <Tab label="Timeline" />
            <Tab label="Assessments" />
          </Tabs>
        </Box>
        <CardContent>
          {renderTabContent()}
        </CardContent>
      </Card>
    </Box>
  );
};

export default CandidateDetails;
