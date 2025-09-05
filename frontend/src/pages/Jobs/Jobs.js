import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { jobService } from '../../services/jobService';
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

const Jobs = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedJob, setSelectedJob] = useState(null);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setLoading(true);
        const response = await jobService.getJobs();
        setJobs(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch jobs. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []);

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

  const handleDeleteJob = async () => {
    if (selectedJob) {
      try {
        await jobService.deleteJob(selectedJob.id);
        setJobs(jobs.filter(job => job.id !== selectedJob.id));
      } catch (err) {
        console.error('Failed to delete job:', err);
        // Optionally, show an error message to the user
      }
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
    (job.location && job.location.toLowerCase().includes(searchTerm.toLowerCase()))
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
                      {job.salary_min && job.salary_max ? `${job.salary_min} - ${job.salary_max} ${job.currency}` : 'Not specified'}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <PeopleIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">
                      {job.candidate_count} applicants
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
                    label={job.employment_type}
                    variant="outlined"
                    size="small"
                  />
                </Box>

                {/* Description */}
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {job.description}
                </Typography>


                {/* Posted Date */}
                <Typography variant="caption" color="text.secondary">
                  Posted {new Date(job.created_at).toLocaleDateString()}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Loading and Error States */}
      {loading && <Typography>Loading jobs...</Typography>}
      {error && <Typography color="error">{error}</Typography>}

      {/* Empty State */}
      {!loading && !error && filteredJobs.length === 0 && (
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
