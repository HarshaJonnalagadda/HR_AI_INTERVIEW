import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Paper,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp,
  People,
  Work,
  Event,
  Phone,
  CheckCircle,
  Schedule,
  Cancel,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

// Mock data for demonstration
const statsData = [
  {
    title: 'Total Jobs',
    value: '24',
    change: '+12%',
    icon: <Work />,
    color: '#1976d2',
  },
  {
    title: 'Active Candidates',
    value: '156',
    change: '+8%',
    icon: <People />,
    color: '#2e7d32',
  },
  {
    title: 'Interviews Scheduled',
    value: '18',
    change: '+25%',
    icon: <Event />,
    color: '#ed6c02',
  },
  {
    title: 'Calls Made',
    value: '89',
    change: '+15%',
    icon: <Phone />,
    color: '#9c27b0',
  },
];

const monthlyData = [
  { month: 'Jan', applications: 45, interviews: 12, hires: 3 },
  { month: 'Feb', applications: 52, interviews: 15, hires: 4 },
  { month: 'Mar', applications: 48, interviews: 18, hires: 5 },
  { month: 'Apr', applications: 61, interviews: 22, hires: 6 },
  { month: 'May', applications: 55, interviews: 19, hires: 4 },
  { month: 'Jun', applications: 67, interviews: 25, hires: 7 },
];

const pipelineData = [
  { name: 'Applied', value: 156, color: '#8884d8' },
  { name: 'Screening', value: 89, color: '#82ca9d' },
  { name: 'Interview', value: 45, color: '#ffc658' },
  { name: 'Offer', value: 12, color: '#ff7300' },
  { name: 'Hired', value: 7, color: '#00ff00' },
];

const recentActivities = [
  {
    id: 1,
    type: 'interview',
    title: 'Interview scheduled with John Doe',
    subtitle: 'Senior Developer position',
    time: '2 hours ago',
    status: 'scheduled',
  },
  {
    id: 2,
    type: 'application',
    title: 'New application received',
    subtitle: 'Marketing Manager position',
    time: '4 hours ago',
    status: 'new',
  },
  {
    id: 3,
    type: 'call',
    title: 'Voice call completed',
    subtitle: 'Sarah Smith - UI/UX Designer',
    time: '6 hours ago',
    status: 'completed',
  },
  {
    id: 4,
    type: 'hire',
    title: 'Candidate hired',
    subtitle: 'Mike Johnson - Backend Developer',
    time: '1 day ago',
    status: 'success',
  },
];

const Dashboard = () => {
  const getActivityIcon = (type) => {
    switch (type) {
      case 'interview':
        return <Event />;
      case 'application':
        return <People />;
      case 'call':
        return <Phone />;
      case 'hire':
        return <CheckCircle />;
      default:
        return <Schedule />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'scheduled':
        return 'primary';
      case 'new':
        return 'info';
      case 'completed':
        return 'success';
      case 'success':
        return 'success';
      default:
        return 'default';
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Dashboard
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Welcome back! Here's what's happening with your recruitment process.
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {statsData.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: stat.color, mr: 2 }}>
                    {stat.icon}
                  </Avatar>
                  <Box>
                    <Typography variant="h4" fontWeight="bold">
                      {stat.value}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {stat.title}
                    </Typography>
                  </Box>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <TrendingUp sx={{ color: 'success.main', mr: 1, fontSize: 16 }} />
                  <Typography variant="body2" color="success.main">
                    {stat.change} from last month
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* Monthly Trends Chart */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Monthly Trends
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={monthlyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="applications" fill="#8884d8" name="Applications" />
                    <Bar dataKey="interviews" fill="#82ca9d" name="Interviews" />
                    <Bar dataKey="hires" fill="#ffc658" name="Hires" />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Pipeline Overview */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recruitment Pipeline
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={pipelineData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}`}
                    >
                      {pipelineData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activities */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activities
              </Typography>
              <List>
                {recentActivities.map((activity) => (
                  <ListItem key={activity.id} divider>
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: 'primary.main' }}>
                        {getActivityIcon(activity.type)}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={activity.title}
                      secondary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                          <Typography variant="body2" color="text.secondary">
                            {activity.subtitle}
                          </Typography>
                          <Chip
                            label={activity.status}
                            size="small"
                            color={getStatusColor(activity.status)}
                          />
                        </Box>
                      }
                    />
                    <Typography variant="caption" color="text.secondary">
                      {activity.time}
                    </Typography>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                <Grid item xs={6}>
                  <Paper
                    sx={{
                      p: 2,
                      textAlign: 'center',
                      cursor: 'pointer',
                      '&:hover': { bgcolor: 'action.hover' },
                    }}
                  >
                    <Work sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                    <Typography variant="subtitle2">Create Job</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6}>
                  <Paper
                    sx={{
                      p: 2,
                      textAlign: 'center',
                      cursor: 'pointer',
                      '&:hover': { bgcolor: 'action.hover' },
                    }}
                  >
                    <People sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                    <Typography variant="subtitle2">Add Candidate</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6}>
                  <Paper
                    sx={{
                      p: 2,
                      textAlign: 'center',
                      cursor: 'pointer',
                      '&:hover': { bgcolor: 'action.hover' },
                    }}
                  >
                    <Event sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
                    <Typography variant="subtitle2">Schedule Interview</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6}>
                  <Paper
                    sx={{
                      p: 2,
                      textAlign: 'center',
                      cursor: 'pointer',
                      '&:hover': { bgcolor: 'action.hover' },
                    }}
                  >
                    <Phone sx={{ fontSize: 40, color: 'secondary.main', mb: 1 }} />
                    <Typography variant="subtitle2">Make Call</Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
