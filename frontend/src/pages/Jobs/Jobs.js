import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  TextField,
  InputAdornment,
  Fab,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  MoreVert as MoreVertIcon,
  Work as WorkIcon,
  LocationOn as LocationIcon,
  AttachMoney as MoneyIcon,
  People as PeopleIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
} from '@mui/icons-material';

// Mock data for jobs
const mockJobs = [
  {
    id: 1,
    title: 'Senior Full Stack Developer',
    company: 'TechCorp India',
    location: 'Bangalore, India',
    type: 'Full-time',
    salary: '₹15-25 LPA',
    status: 'active',
    applicants: 24,
    posted: '2 days ago',
    description: 'Looking for an experienced full stack developer with React and Node.js expertise.',
    requirements: ['React.js', 'Node.js', 'MongoDB', '5+ years experience'],
  },
  {
    id: 2,
    title: 'Product Manager',
    company: 'StartupXYZ',
    location: 'Mumbai, India',
    type: 'Full-time',
    salary: '₹20-30 LPA',
    status: 'active',
    applicants: 18,
    posted: '5 days ago',
    description: 'Seeking a product manager to lead our mobile app development initiatives.',
    requirements: ['Product Management', 'Agile', 'Mobile Apps', '3+ years experience'],
  },
  {
    id: 3,
    title: 'UI/UX Designer',
    company: 'DesignStudio',
    location: 'Delhi, India',
    type: 'Contract',
    salary: '₹8-12 LPA',
    status: 'paused',
    applicants: 31,
    posted: '1 week ago',
    description: 'Creative UI/UX designer needed for e-commerce platform redesign.',
    requirements: ['Figma', 'Adobe Creative Suite', 'User Research', '2+ years experience'],
  },
  {
    id: 4,
    title: 'Data Scientist',
    company: 'AI Solutions Ltd',
    location: 'Hyderabad, India',
    type: 'Full-time',
    salary: '₹18-28 LPA',
    status: 'active',
    applicants: 12,
    posted: '3 days ago',
    description: 'Data scientist role focusing on machine learning and predictive analytics.',
    requirements: ['Python', 'Machine Learning', 'SQL', 'Statistics', '4+ years experience'],
  },
];

const Jobs = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState(mockJobs);
  const [searchTerm, setSearchTerm] = useState('');
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedJob, setSelectedJob] = useState(null);

  const handleMenuOpen = (event, job) => {
    setAnchorEl(event.currentTarget);
    setSelectedJob(job);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedJob(null);
  };

  const handleViewJob = () => {
    if (selectedJob) {
      navigate(`/jobs/${selectedJob.id}`);
    }
    handleMenuClose();
  };

  const handleEditJob = () => {
    if (selectedJob) {
      navigate(`/jobs/${selectedJob.id}/edit`);
    }
    handleMenuClose();
  };

  const handleDeleteJob = () => {
    if (selectedJob) {
      setJobs(jobs.filter(job => job.id !== selectedJob.id));
    }
    handleMenuClose();
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'paused':
        return 'warning';
      case 'closed':
        return 'error';
      default:
        return 'default';
    }
  };

  const filteredJobs = jobs.filter(job =>
    job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" fontWeight="bold">
            Jobs
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Manage your job postings and track applications
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/jobs/create')}
          sx={{ borderRadius: 2 }}
        >
          Create Job
        </Button>
      </Box>

      {/* Search */}
      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search jobs by title, company, or location..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
          sx={{ maxWidth: 500 }}
        />
      </Box>

      {/* Jobs Grid */}
      <Grid container spacing={3}>
        {filteredJobs.map((job) => (
          <Grid item xs={12} md={6} lg={4} key={job.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
              }}
              onClick={() => navigate(`/jobs/${job.id}`)}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                {/* Header */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      {job.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {job.company}
                    </Typography>
                  </Box>
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleMenuOpen(e, job);
                    }}
                  >
                    <MoreVertIcon />
                  </IconButton>
                </Box>

                {/* Job Details */}
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <LocationIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">
                      {job.location}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <MoneyIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">
                      {job.salary}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <PeopleIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">
                      {job.applicants} applicants
                    </Typography>
                  </Box>
                </Box>

                {/* Status and Type */}
                <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                  <Chip
                    label={job.status}
                    color={getStatusColor(job.status)}
                    size="small"
                  />
                  <Chip
                    label={job.type}
                    variant="outlined"
                    size="small"
                  />
                </Box>

                {/* Description */}
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {job.description}
                </Typography>

                {/* Requirements */}
                <Box sx={{ mb: 2 }}>
                  <Typography variant="caption" color="text.secondary" gutterBottom>
                    Key Requirements:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                    {job.requirements.slice(0, 3).map((req, index) => (
                      <Chip
                        key={index}
                        label={req}
                        size="small"
                        variant="outlined"
                        sx={{ fontSize: '0.7rem' }}
                      />
                    ))}
                    {job.requirements.length > 3 && (
                      <Chip
                        label={`+${job.requirements.length - 3} more`}
                        size="small"
                        variant="outlined"
                        sx={{ fontSize: '0.7rem' }}
                      />
                    )}
                  </Box>
                </Box>

                {/* Posted Date */}
                <Typography variant="caption" color="text.secondary">
                  Posted {job.posted}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Empty State */}
      {filteredJobs.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <WorkIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No jobs found
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            {searchTerm ? 'Try adjusting your search criteria' : 'Create your first job posting to get started'}
          </Typography>
          {!searchTerm && (
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => navigate('/jobs/create')}
            >
              Create Job
            </Button>
          )}
        </Box>
      )}

      {/* Floating Action Button for Mobile */}
      <Fab
        color="primary"
        aria-label="add job"
        sx={{
          position: 'fixed',
          bottom: 16,
          right: 16,
          display: { xs: 'flex', md: 'none' },
        }}
        onClick={() => navigate('/jobs/create')}
      >
        <AddIcon />
      </Fab>

      {/* Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleViewJob}>
          <ViewIcon sx={{ mr: 2 }} />
          View Details
        </MenuItem>
        <MenuItem onClick={handleEditJob}>
          <EditIcon sx={{ mr: 2 }} />
          Edit Job
        </MenuItem>
        <MenuItem onClick={handleDeleteJob} sx={{ color: 'error.main' }}>
          <DeleteIcon sx={{ mr: 2 }} />
          Delete Job
        </MenuItem>
      </Menu>
    </Box>
  );
};

export default Jobs;
