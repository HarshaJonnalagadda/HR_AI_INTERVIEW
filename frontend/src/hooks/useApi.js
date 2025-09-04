import { useQuery, useMutation, useQueryClient } from 'react-query';
import {
  jobsService,
  candidatesService,
  interviewsService,
  voiceService,
  dashboardService,
  outreachService,
  calendarService,
} from '../services/apiService';
import toast from 'react-hot-toast';

// Jobs hooks
export const useJobs = (params) => {
  return useQuery(['jobs', params], () => jobsService.getJobs(params), {
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useJob = (id) => {
  return useQuery(['job', id], () => jobsService.getJob(id), {
    enabled: !!id,
  });
};

export const useCreateJob = () => {
  const queryClient = useQueryClient();
  return useMutation(jobsService.createJob, {
    onSuccess: () => {
      queryClient.invalidateQueries(['jobs']);
      toast.success('Job created successfully!');
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to create job');
    },
  });
};

export const useUpdateJob = () => {
  const queryClient = useQueryClient();
  return useMutation(
    ({ id, data }) => jobsService.updateJob(id, data),
    {
      onSuccess: (data, variables) => {
        queryClient.invalidateQueries(['jobs']);
        queryClient.invalidateQueries(['job', variables.id]);
        toast.success('Job updated successfully!');
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Failed to update job');
      },
    }
  );
};

export const useDeleteJob = () => {
  const queryClient = useQueryClient();
  return useMutation(jobsService.deleteJob, {
    onSuccess: () => {
      queryClient.invalidateQueries(['jobs']);
      toast.success('Job deleted successfully!');
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to delete job');
    },
  });
};

// Candidates hooks
export const useCandidates = (params) => {
  return useQuery(['candidates', params], () => candidatesService.getCandidates(params), {
    staleTime: 5 * 60 * 1000,
  });
};

export const useCandidate = (id) => {
  return useQuery(['candidate', id], () => candidatesService.getCandidate(id), {
    enabled: !!id,
  });
};

export const useCreateCandidate = () => {
  const queryClient = useQueryClient();
  return useMutation(candidatesService.createCandidate, {
    onSuccess: () => {
      queryClient.invalidateQueries(['candidates']);
      toast.success('Candidate added successfully!');
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to add candidate');
    },
  });
};

export const useUpdateCandidate = () => {
  const queryClient = useQueryClient();
  return useMutation(
    ({ id, data }) => candidatesService.updateCandidate(id, data),
    {
      onSuccess: (data, variables) => {
        queryClient.invalidateQueries(['candidates']);
        queryClient.invalidateQueries(['candidate', variables.id]);
        toast.success('Candidate updated successfully!');
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Failed to update candidate');
      },
    }
  );
};

export const useSourceCandidates = () => {
  const queryClient = useQueryClient();
  return useMutation(
    ({ jobId, criteria }) => candidatesService.sourceCandidates(jobId, criteria),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['candidates']);
        toast.success('Candidate sourcing initiated!');
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Failed to source candidates');
      },
    }
  );
};

// Interviews hooks
export const useInterviews = (params) => {
  return useQuery(['interviews', params], () => interviewsService.getInterviews(params), {
    staleTime: 5 * 60 * 1000,
  });
};

export const useInterview = (id) => {
  return useQuery(['interview', id], () => interviewsService.getInterview(id), {
    enabled: !!id,
  });
};

export const useScheduleInterview = () => {
  const queryClient = useQueryClient();
  return useMutation(interviewsService.scheduleInterview, {
    onSuccess: () => {
      queryClient.invalidateQueries(['interviews']);
      toast.success('Interview scheduled successfully!');
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to schedule interview');
    },
  });
};

export const useUpdateInterview = () => {
  const queryClient = useQueryClient();
  return useMutation(
    ({ id, data }) => interviewsService.updateInterview(id, data),
    {
      onSuccess: (data, variables) => {
        queryClient.invalidateQueries(['interviews']);
        queryClient.invalidateQueries(['interview', variables.id]);
        toast.success('Interview updated successfully!');
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Failed to update interview');
      },
    }
  );
};

export const useSubmitFeedback = () => {
  const queryClient = useQueryClient();
  return useMutation(
    ({ id, feedback }) => interviewsService.submitFeedback(id, feedback),
    {
      onSuccess: (data, variables) => {
        queryClient.invalidateQueries(['interview', variables.id]);
        toast.success('Feedback submitted successfully!');
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Failed to submit feedback');
      },
    }
  );
};

// Voice calls hooks
export const useInitiateCall = () => {
  return useMutation(
    ({ candidateId, callData }) => voiceService.initiateCall(candidateId, callData),
    {
      onSuccess: () => {
        toast.success('Call initiated successfully!');
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Failed to initiate call');
      },
    }
  );
};

export const useEndCall = () => {
  return useMutation(
    ({ callId, callData }) => voiceService.endCall(callId, callData),
    {
      onSuccess: () => {
        toast.success('Call ended and notes saved!');
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Failed to end call');
      },
    }
  );
};

// Dashboard hooks
export const useDashboardStats = () => {
  return useQuery(['dashboard', 'stats'], dashboardService.getDashboardStats, {
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

export const useRecentActivities = () => {
  return useQuery(['dashboard', 'activities'], dashboardService.getRecentActivities, {
    staleTime: 1 * 60 * 1000, // 1 minute
  });
};

export const useAnalytics = (period = '30d') => {
  return useQuery(['dashboard', 'analytics', period], () => dashboardService.getAnalytics(period), {
    staleTime: 5 * 60 * 1000,
  });
};

// Outreach hooks
export const useSendEmail = () => {
  return useMutation(
    ({ candidateId, emailData }) => outreachService.sendEmail(candidateId, emailData),
    {
      onSuccess: () => {
        toast.success('Email sent successfully!');
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Failed to send email');
      },
    }
  );
};

export const useSendSMS = () => {
  return useMutation(
    ({ candidateId, smsData }) => outreachService.sendSMS(candidateId, smsData),
    {
      onSuccess: () => {
        toast.success('SMS sent successfully!');
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Failed to send SMS');
      },
    }
  );
};

export const useGenerateMessage = () => {
  return useMutation(
    ({ candidateId, messageType, context }) => 
      outreachService.generateMessage(candidateId, messageType, context),
    {
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Failed to generate message');
      },
    }
  );
};

// Calendar hooks
export const useAvailability = (date) => {
  return useQuery(['calendar', 'availability', date], () => calendarService.getAvailability(date), {
    enabled: !!date,
    staleTime: 5 * 60 * 1000,
  });
};

export const useCreateEvent = () => {
  const queryClient = useQueryClient();
  return useMutation(calendarService.createEvent, {
    onSuccess: () => {
      queryClient.invalidateQueries(['calendar']);
      toast.success('Event created successfully!');
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to create event');
    },
  });
};
