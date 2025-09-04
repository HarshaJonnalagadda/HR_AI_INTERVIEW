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
  Avatar,
  TextField,
  InputAdornment,
  Menu,
  MenuItem,
  IconButton,
  Fab,
  FormControl,
  InputLabel,
  Select,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  MoreVert as MoreVertIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  Work as WorkIcon,
  LocationOn as LocationIcon,
  Star as StarIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';

// Mock data for candidates
const mockCandidates = [
  {
    id: 1,
    name: 'John Doe',
    email: 'john.doe@email.com',
    phone: '+91 9876543210',
    location: 'Bangalore, India',
    experience: '6 years',
    currentRole: 'Senior Developer',
    currentCompany: 'Tech Solutions',
    skills: ['React', 'Node.js', 'MongoDB', 'JavaScript', 'AWS'],
    status: 'active',
    stage: 'interview',
    jobTitle: 'Senior Full Stack Developer',
    rating: 4.5,
    lastActivity: '2 hours ago',
    avatar: 'J',
  },
  {
    id: 2,
    name: 'Sarah Smith',
    email: 'sarah.smith@email.com',
    phone: '+91 9876543211',
    location: 'Mumbai, India',
    experience: '4 years',
    currentRole: 'Frontend Developer',
    currentCompany: 'Digital Agency',
    skills: ['React', 'Vue.js', 'CSS', 'JavaScript', 'Figma'],
    status: 'active',
    stage: 'screening',
    jobTitle: 'UI/UX Developer',
    rating: 4.2,
    lastActivity: '1 day ago',
    avatar: 'S',
  },
  {
    id: 3,
    name: 'Mike Johnson',
    email: 'mike.johnson@email.com',
    phone: '+91 9876543212',
    location: 'Delhi, India',
    experience: '7 years',
    currentRole: 'Tech Lead',
    currentCompany: 'Enterprise Corp',
    skills: ['Java', 'Spring Boot', 'Microservices', 'Docker', 'Kubernetes'],
    status: 'hired',
    stage: 'hired',
    jobTitle: 'Backend Architect',
    rating: 4.8,
    lastActivity: '3 days ago',
    avatar: 'M',
  },
  {
    id: 4,
    name: 'Priya Sharma',
    email: 'priya.sharma@email.com',
    phone: '+91 9876543213',
    location: 'Hyderabad, India',
    experience: '3 years',
    currentRole: 'Data Analyst',
    currentCompany: 'Analytics Inc',
    skills: ['Python', 'SQL', 'Tableau', 'Machine Learning', 'Statistics'],
    status: 'active',
    stage: 'applied',
    jobTitle: 'Data Scientist',
    rating: 4.0,
    lastActivity: '5 hours ago',
    avatar: 'P',
  },
];

const Candidates = () => {
  const navigate = useNavigate();
  const [candidates, setCandidates] = useState(mockCandidates);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [stageFilter, setStageFilter] = useState('all');
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  const handleMenuOpen = (event, candidate) => {
    setAnchorEl(event.currentTarget);
    setSelectedCandidate(candidate);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedCandidate(null);
  };

  const handleViewCandidate = () => {
    if (selectedCandidate) {
      navigate(`/candidates/${selectedCandidate.id}`);
    }
    handleMenuClose();
  };

  const handleScheduleInterview = () => {
    if (selectedCandidate) {
      navigate(`/interviews/schedule?candidateId=${selectedCandidate.id}`);
    }
    handleMenuClose();
  };

  const handleMakeCall = () => {
    if (selectedCandidate) {
      navigate(`/voice-call/${selectedCandidate.id}`);
    }
    handleMenuClose();
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'hired':
        return 'primary';
      case 'rejected':
        return 'error';
      case 'on-hold':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStageColor = (stage) => {
    switch (stage) {
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

  const filteredCandidates = candidates.filter(candidate => {
    const matchesSearch = 
      candidate.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.currentRole.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.skills.some(skill => skill.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesStatus = statusFilter === 'all' || candidate.status === statusFilter;
    const matchesStage = stageFilter === 'all' || candidate.stage === stageFilter;
    
    return matchesSearch && matchesStatus && matchesStage;
  });

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<StarIcon key={i} sx={{ fontSize: 16, color: 'gold' }} />);
    }
    
    if (hasHalfStar) {
      stars.push(<StarIcon key="half" sx={{ fontSize: 16, color: 'gold', opacity: 0.5 }} />);
    }
    
    return stars;
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" fontWeight="bold">
            Candidates
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Manage and track candidate applications
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/candidates/add')}
          sx={{ borderRadius: 2 }}
        >
          Add Candidate
        </Button>
      </Box>

      {/* Filters */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            placeholder="Search candidates by name, email, role, or skills..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <FormControl fullWidth>
            <InputLabel>Status</InputLabel>
            <Select
              value={statusFilter}
              label="Status"
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <MenuItem value="all">All Status</MenuItem>
              <MenuItem value="active">Active</MenuItem>
              <MenuItem value="hired">Hired</MenuItem>
              <MenuItem value="rejected">Rejected</MenuItem>
              <MenuItem value="on-hold">On Hold</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={3}>
          <FormControl fullWidth>
            <InputLabel>Stage</InputLabel>
            <Select
              value={stageFilter}
              label="Stage"
              onChange={(e) => setStageFilter(e.target.value)}
            >
              <MenuItem value="all">All Stages</MenuItem>
              <MenuItem value="applied">Applied</MenuItem>
              <MenuItem value="screening">Screening</MenuItem>
              <MenuItem value="interview">Interview</MenuItem>
              <MenuItem value="hired">Hired</MenuItem>
              <MenuItem value="rejected">Rejected</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      {/* Candidates Grid */}
      <Grid container spacing={3}>
        {filteredCandidates.map((candidate) => (
          <Grid item xs={12} md={6} lg={4} key={candidate.id}>
            <Card
              sx={{
                height: '100%',
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
              }}
              onClick={() => navigate(`/candidates/${candidate.id}`)}
            >
              <CardContent>
                {/* Header */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar sx={{ bgcolor: 'primary.main', width: 48, height: 48 }}>
                      {candidate.avatar}
                    </Avatar>
                    <Box>
                      <Typography variant="h6" fontWeight="bold">
                        {candidate.name}
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        {renderStars(candidate.rating)}
                        <Typography variant="caption" color="text.secondary" sx={{ ml: 0.5 }}>
                          ({candidate.rating})
                        </Typography>
                      </Box>
                    </Box>
                  </Box>
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleMenuOpen(e, candidate);
                    }}
                  >
                    <MoreVertIcon />
                  </IconButton>
                </Box>

                {/* Contact Info */}
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <EmailIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary" noWrap>
                      {candidate.email}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <PhoneIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">
                      {candidate.phone}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <LocationIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">
                      {candidate.location}
                    </Typography>
                  </Box>
                </Box>

                {/* Current Role */}
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    {candidate.currentRole}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {candidate.currentCompany} • {candidate.experience}
                  </Typography>
                </Box>

                {/* Applied For */}
                <Box sx={{ mb: 2 }}>
                  <Typography variant="caption" color="text.secondary">
                    Applied for:
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {candidate.jobTitle}
                  </Typography>
                </Box>

                {/* Status and Stage */}
                <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                  <Chip
                    label={candidate.status}
                    color={getStatusColor(candidate.status)}
                    size="small"
                  />
                  <Chip
                    label={candidate.stage}
                    color={getStageColor(candidate.stage)}
                    variant="outlined"
                    size="small"
                  />
                </Box>

                {/* Skills */}
                <Box sx={{ mb: 2 }}>
                  <Typography variant="caption" color="text.secondary" gutterBottom>
                    Skills:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                    {candidate.skills.slice(0, 4).map((skill, index) => (
                      <Chip
                        key={index}
                        label={skill}
                        size="small"
                        variant="outlined"
                        sx={{ fontSize: '0.7rem' }}
                      />
                    ))}
                    {candidate.skills.length > 4 && (
                      <Chip
                        label={`+${candidate.skills.length - 4}`}
                        size="small"
                        variant="outlined"
                        sx={{ fontSize: '0.7rem' }}
                      />
                    )}
                  </Box>
                </Box>

                {/* Last Activity */}
                <Typography variant="caption" color="text.secondary">
                  Last activity: {candidate.lastActivity}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Empty State */}
      {filteredCandidates.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <WorkIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No candidates found
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            {searchTerm || statusFilter !== 'all' || stageFilter !== 'all' 
              ? 'Try adjusting your search or filter criteria' 
              : 'Add your first candidate to get started'}
          </Typography>
          {!searchTerm && statusFilter === 'all' && stageFilter === 'all' && (
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => navigate('/candidates/add')}
            >
              Add Candidate
            </Button>
          )}
        </Box>
      )}

      {/* Floating Action Button for Mobile */}
      <Fab
        color="primary"
        aria-label="add candidate"
        sx={{
          position: 'fixed',
          bottom: 16,
          right: 16,
          display: { xs: 'flex', md: 'none' },
        }}
        onClick={() => navigate('/candidates/add')}
      >
        <AddIcon />
      </Fab>

      {/* Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleViewCandidate}>
          <WorkIcon sx={{ mr: 2 }} />
          View Profile
        </MenuItem>
        <MenuItem onClick={handleScheduleInterview}>
          <ScheduleIcon sx={{ mr: 2 }} />
          Schedule Interview
        </MenuItem>
        <MenuItem onClick={handleMakeCall}>
          <PhoneIcon sx={{ mr: 2 }} />
          Make Call
        </MenuItem>
      </Menu>
    </Box>
  );
};

export default Candidates;
