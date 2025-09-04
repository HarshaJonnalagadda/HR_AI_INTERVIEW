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
  VideoCall as VideoCallIcon,
  Phone as PhoneIcon,
  Event as EventIcon,
  Person as PersonIcon,
  Schedule as ScheduleIcon,
  Edit as EditIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';

// Mock data for interviews
const mockInterviews = [
  {
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
  },
  {
    id: 2,
    candidateName: 'Priya Sharma',
    candidateId: 4,
    jobTitle: 'Data Scientist',
    jobId: 4,
    type: 'hr',
    mode: 'phone',
    date: '2024-01-22',
    time: '2:00 PM',
    duration: 45,
    status: 'scheduled',
    interviewer: 'Mike Johnson',
    interviewerId: 2,
    location: 'Phone Call',
    notes: 'HR screening and culture fit assessment',
    candidateAvatar: 'P',
  },
  {
    id: 3,
    candidateName: 'Sarah Smith',
    candidateId: 2,
    jobTitle: 'UI/UX Developer',
    jobId: 2,
    type: 'design',
    mode: 'in-person',
    date: '2024-01-23',
    time: '11:00 AM',
    duration: 90,
    status: 'completed',
    interviewer: 'Alex Chen',
    interviewerId: 3,
    location: 'Design Studio',
    notes: 'Portfolio review and design challenge',
    candidateAvatar: 'S',
  },
  {
    id: 4,
    candidateName: 'Mike Johnson',
    candidateId: 3,
    jobTitle: 'Backend Architect',
    jobId: 3,
    type: 'technical',
    mode: 'video',
    date: '2024-01-24',
    time: '3:00 PM',
    duration: 75,
    status: 'cancelled',
    interviewer: 'David Kumar',
    interviewerId: 4,
    location: 'Zoom Meeting',
    notes: 'System design and architecture discussion',
    candidateAvatar: 'M',
  },
];

const Interviews = () => {
  const navigate = useNavigate();
  const [interviews, setInterviews] = useState(mockInterviews);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedInterview, setSelectedInterview] = useState(null);

  const handleMenuOpen = (event, interview) => {
    setAnchorEl(event.currentTarget);
    setSelectedInterview(interview);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedInterview(null);
  };

  const handleViewInterview = () => {
    if (selectedInterview) {
      navigate(`/interviews/${selectedInterview.id}`);
    }
    handleMenuClose();
  };

  const handleEditInterview = () => {
    if (selectedInterview) {
      navigate(`/interviews/${selectedInterview.id}/edit`);
    }
    handleMenuClose();
  };

  const handleCancelInterview = () => {
    if (selectedInterview) {
      setInterviews(interviews.map(interview => 
        interview.id === selectedInterview.id 
          ? { ...interview, status: 'cancelled' }
          : interview
      ));
    }
    handleMenuClose();
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

  const getTypeColor = (type) => {
    switch (type) {
      case 'technical':
        return 'info';
      case 'hr':
        return 'secondary';
      case 'design':
        return 'warning';
      case 'final':
        return 'success';
      default:
        return 'default';
    }
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

  const filteredInterviews = interviews.filter(interview => {
    const matchesSearch = 
      interview.candidateName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      interview.jobTitle.toLowerCase().includes(searchTerm.toLowerCase()) ||
      interview.interviewer.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || interview.status === statusFilter;
    const matchesType = typeFilter === 'all' || interview.type === typeFilter;
    
    return matchesSearch && matchesStatus && matchesType;
  });

  const isUpcoming = (date, time) => {
    const interviewDateTime = new Date(`${date} ${time}`);
    return interviewDateTime > new Date();
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" fontWeight="bold">
            Interviews
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Manage and track interview schedules
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/interviews/schedule')}
          sx={{ borderRadius: 2 }}
        >
          Schedule Interview
        </Button>
      </Box>

      {/* Filters */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            placeholder="Search interviews by candidate, job, or interviewer..."
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
              <MenuItem value="scheduled">Scheduled</MenuItem>
              <MenuItem value="completed">Completed</MenuItem>
              <MenuItem value="cancelled">Cancelled</MenuItem>
              <MenuItem value="rescheduled">Rescheduled</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={3}>
          <FormControl fullWidth>
            <InputLabel>Type</InputLabel>
            <Select
              value={typeFilter}
              label="Type"
              onChange={(e) => setTypeFilter(e.target.value)}
            >
              <MenuItem value="all">All Types</MenuItem>
              <MenuItem value="technical">Technical</MenuItem>
              <MenuItem value="hr">HR</MenuItem>
              <MenuItem value="design">Design</MenuItem>
              <MenuItem value="final">Final</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      {/* Interviews Grid */}
      <Grid container spacing={3}>
        {filteredInterviews.map((interview) => (
          <Grid item xs={12} md={6} lg={4} key={interview.id}>
            <Card
              sx={{
                height: '100%',
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
                border: isUpcoming(interview.date, interview.time) && interview.status === 'scheduled' 
                  ? '2px solid' 
                  : 'none',
                borderColor: 'primary.main',
              }}
              onClick={() => navigate(`/interviews/${interview.id}`)}
            >
              <CardContent>
                {/* Header */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar sx={{ bgcolor: 'primary.main' }}>
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
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleMenuOpen(e, interview);
                    }}
                  >
                    <MoreVertIcon />
                  </IconButton>
                </Box>

                {/* Interview Details */}
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <EventIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">
                      {new Date(interview.date).toLocaleDateString()} at {interview.time}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    {getModeIcon(interview.mode)}
                    <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                      {interview.location} • {interview.duration} min
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <PersonIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">
                      Interviewer: {interview.interviewer}
                    </Typography>
                  </Box>
                </Box>

                {/* Status and Type */}
                <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                  <Chip
                    label={interview.status}
                    color={getStatusColor(interview.status)}
                    size="small"
                  />
                  <Chip
                    label={interview.type}
                    color={getTypeColor(interview.type)}
                    variant="outlined"
                    size="small"
                  />
                  <Chip
                    label={interview.mode}
                    variant="outlined"
                    size="small"
                  />
                </Box>

                {/* Notes */}
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {interview.notes}
                </Typography>

                {/* Upcoming indicator */}
                {isUpcoming(interview.date, interview.time) && interview.status === 'scheduled' && (
                  <Chip
                    label="Upcoming"
                    color="warning"
                    size="small"
                    sx={{ fontWeight: 'bold' }}
                  />
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Empty State */}
      {filteredInterviews.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <ScheduleIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No interviews found
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            {searchTerm || statusFilter !== 'all' || typeFilter !== 'all' 
              ? 'Try adjusting your search or filter criteria' 
              : 'Schedule your first interview to get started'}
          </Typography>
          {!searchTerm && statusFilter === 'all' && typeFilter === 'all' && (
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => navigate('/interviews/schedule')}
            >
              Schedule Interview
            </Button>
          )}
        </Box>
      )}

      {/* Floating Action Button for Mobile */}
      <Fab
        color="primary"
        aria-label="schedule interview"
        sx={{
          position: 'fixed',
          bottom: 16,
          right: 16,
          display: { xs: 'flex', md: 'none' },
        }}
        onClick={() => navigate('/interviews/schedule')}
      >
        <AddIcon />
      </Fab>

      {/* Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleViewInterview}>
          <EventIcon sx={{ mr: 2 }} />
          View Details
        </MenuItem>
        <MenuItem onClick={handleEditInterview}>
          <EditIcon sx={{ mr: 2 }} />
          Edit Interview
        </MenuItem>
        {selectedInterview?.status === 'scheduled' && (
          <MenuItem onClick={handleCancelInterview} sx={{ color: 'error.main' }}>
            <CancelIcon sx={{ mr: 2 }} />
            Cancel Interview
          </MenuItem>
        )}
      </Menu>
    </Box>
  );
};

export default Interviews;
