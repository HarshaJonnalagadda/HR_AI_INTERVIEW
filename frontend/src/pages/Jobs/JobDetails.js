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
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Divider,
  Tab,
  Tabs,
  Paper,
  LinearProgress,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Edit as EditIcon,
  People as PeopleIcon,
  LocationOn as LocationIcon,
  AttachMoney as MoneyIcon,
  Work as WorkIcon,
  Schedule as ScheduleIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';

// Mock data for job details
const mockJob = {
  id: 1,
  title: 'Senior Full Stack Developer',
  company: 'TechCorp India',
  location: 'Bangalore, India',
  type: 'Full-time',
  department: 'Engineering',
  experience_level: 'Senior Level',
  salary: '₹15-25 LPA',
  status: 'active',
  posted: '2 days ago',
  description: `We are looking for an experienced Senior Full Stack Developer to join our dynamic team. You will be responsible for developing and maintaining web applications using modern technologies.

Key Responsibilities:
• Design and develop scalable web applications
• Collaborate with cross-functional teams
• Mentor junior developers
• Participate in code reviews and technical discussions
• Ensure high-quality code and best practices

What We Offer:
• Competitive salary and benefits
• Flexible working hours
• Professional development opportunities
• Modern office environment
• Health insurance and wellness programs`,
  requirements: [
    'React.js',
    'Node.js',
    'MongoDB',
    'JavaScript/TypeScript',
    '5+ years experience',
    'RESTful APIs',
    'Git',
    'Agile methodology'
  ],
  applicants: [
    {
      id: 1,
      name: 'John Doe',
      email: 'john.doe@email.com',
      experience: '6 years',
      skills: ['React', 'Node.js', 'MongoDB'],
      status: 'applied',
      appliedDate: '2024-01-15',
      avatar: 'J',
    },
    {
      id: 2,
      name: 'Sarah Smith',
      email: 'sarah.smith@email.com',
      experience: '4 years',
      skills: ['React', 'Python', 'PostgreSQL'],
      status: 'screening',
      appliedDate: '2024-01-14',
      avatar: 'S',
    },
    {
      id: 3,
      name: 'Mike Johnson',
      email: 'mike.johnson@email.com',
      experience: '7 years',
      skills: ['Vue.js', 'Node.js', 'MySQL'],
      status: 'interview',
      appliedDate: '2024-01-13',
      avatar: 'M',
    },
  ],
  analytics: {
    totalViews: 245,
    totalApplications: 24,
    conversionRate: 9.8,
    avgTimeToApply: '3.2 days',
  },
};

const JobDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const job = mockJob; // In real app, fetch by id

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'applied':
        return 'info';
      case 'screening':
        return 'warning';
      case 'interview':
        return 'primary';
      case 'hired':
        return 'success';
      case 'rejected':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'applied':
        return 'Applied';
      case 'screening':
        return 'Screening';
      case 'interview':
        return 'Interview';
      case 'hired':
        return 'Hired';
      case 'rejected':
        return 'Rejected';
      default:
        return status;
    }
  };

  const renderTabContent = () => {
    switch (tabValue) {
      case 0:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Job Description
            </Typography>
            <Typography variant="body1" paragraph sx={{ whiteSpace: 'pre-line' }}>
              {job.description}
            </Typography>
            
            <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
              Requirements
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {job.requirements.map((requirement, index) => (
                <Chip
                  key={index}
                  label={requirement}
                  variant="outlined"
                  color="primary"
                />
              ))}
            </Box>
          </Box>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Applicants ({job.applicants.length})
            </Typography>
            <List>
              {job.applicants.map((applicant, index) => (
                <React.Fragment key={applicant.id}>
                  <ListItem
                    sx={{
                      cursor: 'pointer',
                      borderRadius: 2,
                      '&:hover': { bgcolor: 'action.hover' },
                    }}
                    onClick={() => navigate(`/candidates/${applicant.id}`)}
                  >
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: 'primary.main' }}>
                        {applicant.avatar}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={applicant.name}
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            {applicant.email} • {applicant.experience} experience
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 0.5, mt: 0.5 }}>
                            {applicant.skills.slice(0, 3).map((skill, idx) => (
                              <Chip
                                key={idx}
                                label={skill}
                                size="small"
                                variant="outlined"
                                sx={{ fontSize: '0.7rem' }}
                              />
                            ))}
                          </Box>
                        </Box>
                      }
                    />
                    <Box sx={{ textAlign: 'right' }}>
                      <Chip
                        label={getStatusText(applicant.status)}
                        color={getStatusColor(applicant.status)}
                        size="small"
                      />
                      <Typography variant="caption" display="block" color="text.secondary">
                        Applied: {new Date(applicant.appliedDate).toLocaleDateString()}
                      </Typography>
                    </Box>
                  </ListItem>
                  {index < job.applicants.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </Box>
        );

      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Job Analytics
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6} md={3}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="h4" color="primary.main">
                    {job.analytics.totalViews}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Views
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="h4" color="success.main">
                    {job.analytics.totalApplications}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Applications
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="h4" color="warning.main">
                    {job.analytics.conversionRate}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Conversion Rate
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="h4" color="info.main">
                    {job.analytics.avgTimeToApply}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Avg. Time to Apply
                  </Typography>
                </Paper>
              </Grid>
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" gutterBottom>
                Application Pipeline
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Applied
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={75}
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2" color="text.secondary">
                      18 candidates
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Screening
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={45}
                      color="warning"
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2" color="text.secondary">
                      8 candidates
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Interview
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={25}
                      color="primary"
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2" color="text.secondary">
                      4 candidates
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Hired
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={10}
                      color="success"
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2" color="text.secondary">
                      2 candidates
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </Box>
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
          onClick={() => navigate('/jobs')}
          sx={{ mr: 2 }}
        >
          Back to Jobs
        </Button>
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h4" fontWeight="bold">
            {job.title}
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {job.company} • Posted {job.posted}
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<EditIcon />}
          onClick={() => navigate(`/jobs/${id}/edit`)}
        >
          Edit Job
        </Button>
      </Box>

      {/* Job Summary Card */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                <Chip label={job.status} color="success" />
                <Chip label={job.type} variant="outlined" />
                <Chip label={job.department} variant="outlined" />
                <Chip label={job.experience_level} variant="outlined" />
              </Box>
              
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, flexWrap: 'wrap' }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <LocationIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Typography variant="body2">{job.location}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <MoneyIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Typography variant="body2">{job.salary}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <PeopleIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Typography variant="body2">{job.applicants.length} applicants</Typography>
                </Box>
              </Box>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Box sx={{ display: 'flex', justifyContent: 'space-around', textAlign: 'center' }}>
                <Box>
                  <Typography variant="h5" color="primary.main">
                    {job.analytics.totalViews}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Views
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h5" color="success.main">
                    {job.analytics.totalApplications}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Applications
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h5" color="warning.main">
                    {job.analytics.conversionRate}%
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Conversion
                  </Typography>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Job Details" />
            <Tab label={`Applicants (${job.applicants.length})`} />
            <Tab label="Analytics" />
          </Tabs>
        </Box>
        <CardContent>
          {renderTabContent()}
        </CardContent>
      </Card>
    </Box>
  );
};

export default JobDetails;
