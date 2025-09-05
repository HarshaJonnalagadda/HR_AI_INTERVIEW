import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  OutlinedInput,
  Stepper,
  Step,
  StepLabel,
  Paper,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Save as SaveIcon,
  Preview as PreviewIcon,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { jobService } from '../../services/jobService';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import toast from 'react-hot-toast';

const schema = yup.object({
  title: yup.string().required('Job title is required'),
  location: yup.string().required('Location is required'),
  employment_type: yup.string().required('Job type is required'),
  salary_min: yup.number().positive('Minimum salary must be positive').required('Minimum salary is required'),
  salary_max: yup.number().positive('Maximum salary must be positive').required('Maximum salary is required'),
  description: yup.string().min(50, 'Description must be at least 50 characters').required('Job description is required'),
  requirements: yup.array().min(1, 'At least one requirement is needed'),
});

const jobTypes = ['Full-time', 'Part-time', 'Contract', 'Internship', 'Remote'];
const experienceLevels = ['Entry Level', 'Mid Level', 'Senior Level', 'Executive'];
const departments = ['Engineering', 'Product', 'Design', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations'];

const steps = ['Basic Information', 'Job Details', 'Requirements', 'Review'];

const CreateJob = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [requirements, setRequirements] = useState([]);
  const [currentRequirement, setCurrentRequirement] = useState('');
  const [loading, setLoading] = useState(false);

  const {
    control,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      title: '',
      location: '',
      employment_type: '',
      department: '',
      experience_level: '',
      salary_min: '',
      salary_max: '',
      description: '',
      requirements: [],
    },
  });

  const watchedValues = watch();

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const addRequirement = () => {
    if (currentRequirement.trim() && !requirements.includes(currentRequirement.trim())) {
      const newRequirements = [...requirements, currentRequirement.trim()];
      setRequirements(newRequirements);
      setValue('requirements', newRequirements);
      setCurrentRequirement('');
    }
  };

  const removeRequirement = (requirementToRemove) => {
    const newRequirements = requirements.filter(req => req !== requirementToRemove);
    setRequirements(newRequirements);
    setValue('requirements', newRequirements);
  };

  const onInvalid = (errors) => {
    console.error('Form validation failed:', errors);
    toast.error('Please fill all required fields correctly.');
  };

  const onSubmit = async (data) => {
    setLoading(true);
    const payload = {
      ...data,
      requirements: data.requirements.join('\n'),
    };

    try {
      await jobService.createJob(payload);
      toast.success('Job created successfully!');
      navigate('/jobs');
    } catch (error) {
      console.error('Failed to create job:', error);
      toast.error(error.response?.data?.detail || 'Failed to create job. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Controller
                name="title"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Job Title"
                    error={!!errors.title}
                    helperText={errors.title?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Controller
                name="location"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Location"
                    error={!!errors.location}
                    helperText={errors.location?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Controller
                name="employment_type"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth error={!!errors.employment_type}>
                    <InputLabel>Job Type</InputLabel>
                    <Select {...field} label="Job Type">
                      {jobTypes.map((type) => (
                        <MenuItem key={type} value={type}>
                          {type}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                )}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Controller
                name="department"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth>
                    <InputLabel>Department</InputLabel>
                    <Select {...field} label="Department">
                      {departments.map((dept) => (
                        <MenuItem key={dept} value={dept}>
                          {dept}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                )}
              />
            </Grid>
          </Grid>
        );

      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Controller
                name="description"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    multiline
                    rows={6}
                    label="Job Description"
                    placeholder="Describe the role, responsibilities, and what makes this opportunity exciting..."
                    error={!!errors.description}
                    helperText={errors.description?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Controller
                name="experience_level"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth>
                    <InputLabel>Experience Level</InputLabel>
                    <Select {...field} label="Experience Level">
                      {experienceLevels.map((level) => (
                        <MenuItem key={level} value={level}>
                          {level}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                )}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <Controller
                name="salary_min"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    type="number"
                    label="Min Salary (₹ LPA)"
                    error={!!errors.salary_min}
                    helperText={errors.salary_min?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <Controller
                name="salary_max"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    type="number"
                    label="Max Salary (₹ LPA)"
                    error={!!errors.salary_max}
                    helperText={errors.salary_max?.message}
                  />
                )}
              />
            </Grid>
          </Grid>
        );

      case 2:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Job Requirements
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Add skills, qualifications, and experience requirements for this position.
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                <TextField
                  fullWidth
                  label="Add Requirement"
                  value={currentRequirement}
                  onChange={(e) => setCurrentRequirement(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      addRequirement();
                    }
                  }}
                  placeholder="e.g., React.js, 3+ years experience, Bachelor's degree"
                />
                <Button
                  variant="contained"
                  onClick={addRequirement}
                  disabled={!currentRequirement.trim()}
                >
                  Add
                </Button>
              </Box>
            </Grid>
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {requirements.map((requirement, index) => (
                  <Chip
                    key={index}
                    label={requirement}
                    onDelete={() => removeRequirement(requirement)}
                    color="primary"
                    variant="outlined"
                  />
                ))}
              </Box>
              {requirements.length === 0 && (
                <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                  No requirements added yet. Add at least one requirement to continue.
                </Typography>
              )}
            </Grid>
          </Grid>
        );

      case 3:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Review Job Details
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Please review all the information before creating the job.
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h5" gutterBottom>
                  {watchedValues.title}
                </Typography>
                <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                  {watchedValues.location}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                  <Chip label={watchedValues.employment_type} color="primary" size="small" />
                  <Chip label={watchedValues.department} variant="outlined" size="small" />
                  <Chip label={watchedValues.experience_level} variant="outlined" size="small" />
                </Box>
                <Typography variant="body1" paragraph>
                  <strong>Salary:</strong> ₹{watchedValues.salary_min} - ₹{watchedValues.salary_max} LPA
                </Typography>
                <Typography variant="body1" paragraph>
                  <strong>Description:</strong>
                </Typography>
                <Typography variant="body2" paragraph>
                  {watchedValues.description}
                </Typography>
                <Typography variant="body1" gutterBottom>
                  <strong>Requirements:</strong>
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {requirements.map((requirement, index) => (
                    <Chip
                      key={index}
                      label={requirement}
                      size="small"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Paper>
            </Grid>
          </Grid>
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
        <Box>
          <Typography variant="h4" fontWeight="bold">
            Create New Job
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Fill in the details to create a new job posting
          </Typography>
        </Box>
      </Box>

      {/* Stepper */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stepper activeStep={activeStep} alternativeLabel>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </CardContent>
      </Card>

      {/* Form */}
      <Card>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit, onInvalid)}>
            {renderStepContent(activeStep)}

            {/* Navigation Buttons */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
              <Button
                disabled={activeStep === 0}
                onClick={handleBack}
              >
                Back
              </Button>
              <Box sx={{ display: 'flex', gap: 2 }}>
                {activeStep === steps.length - 1 ? (
                  <Button
                    type="submit"
                    variant="contained"
                    startIcon={<SaveIcon />}
                    disabled={loading || requirements.length === 0}
                  >
                    {loading ? 'Creating...' : 'Create Job'}
                  </Button>
                ) : (
                  <Button
                    variant="contained"
                    onClick={handleNext}
                    disabled={
                      (activeStep === 0 && (!watchedValues.title || !watchedValues.location || !watchedValues.employment_type)) ||
                      (activeStep === 1 && (!watchedValues.description || !watchedValues.salary_min || !watchedValues.salary_max)) ||
                      (activeStep === 2 && requirements.length === 0)
                    }
                  >
                    Next
                  </Button>
                )}
              </Box>
            </Box>
          </form>
        </CardContent>
      </Card>
    </Box>
  );
};

export default CreateJob;
