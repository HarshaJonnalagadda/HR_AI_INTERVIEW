import api from './authService';

// Jobs API
export const jobsService = {
  async getJobs(params = {}) {
    const response = await api.get('/jobs', { params });
    return response.data;
  },

  async getJob(id) {
    const response = await api.get(`/jobs/${id}`);
    return response.data;
  },

  async createJob(jobData) {
    const response = await api.post('/jobs', jobData);
    return response.data;
  },

  async updateJob(id, jobData) {
    const response = await api.put(`/jobs/${id}`, jobData);
    return response.data;
  },

  async deleteJob(id) {
    const response = await api.delete(`/jobs/${id}`);
    return response.data;
  },

  async analyzeJob(jobData) {
    const response = await api.post('/jobs/analyze', jobData);
    return response.data;
  },
};

// Candidates API
export const candidatesService = {
  async getCandidates(params = {}) {
    const response = await api.get('/candidates', { params });
    return response.data;
  },

  async getCandidate(id) {
    const response = await api.get(`/candidates/${id}`);
    return response.data;
  },

  async createCandidate(candidateData) {
    const response = await api.post('/candidates', candidateData);
    return response.data;
  },

  async updateCandidate(id, candidateData) {
    const response = await api.put(`/candidates/${id}`, candidateData);
    return response.data;
  },

  async deleteCandidate(id) {
    const response = await api.delete(`/candidates/${id}`);
    return response.data;
  },

  async sourceCandidates(jobId, criteria) {
    const response = await api.post('/candidates/source', { job_id: jobId, ...criteria });
    return response.data;
  },

  async matchCandidates(jobId) {
    const response = await api.post(`/candidates/match/${jobId}`);
    return response.data;
  },
};

// Interviews API
export const interviewsService = {
  async getInterviews(params = {}) {
    const response = await api.get('/interviews', { params });
    return response.data;
  },

  async getInterview(id) {
    const response = await api.get(`/interviews/${id}`);
    return response.data;
  },

  async scheduleInterview(interviewData) {
    const response = await api.post('/interviews', interviewData);
    return response.data;
  },

  async updateInterview(id, interviewData) {
    const response = await api.put(`/interviews/${id}`, interviewData);
    return response.data;
  },

  async cancelInterview(id) {
    const response = await api.delete(`/interviews/${id}`);
    return response.data;
  },

  async submitFeedback(id, feedback) {
    const response = await api.post(`/interviews/${id}/feedback`, feedback);
    return response.data;
  },
};

// Voice Calls API
export const voiceService = {
  async initiateCall(candidateId, callData) {
    const response = await api.post('/voice/call', {
      candidate_id: candidateId,
      ...callData,
    });
    return response.data;
  },

  async endCall(callId, callData) {
    const response = await api.post(`/voice/call/${callId}/end`, callData);
    return response.data;
  },

  async getCallHistory(candidateId) {
    const response = await api.get(`/voice/history/${candidateId}`);
    return response.data;
  },
};

// Dashboard API
export const dashboardService = {
  async getDashboardStats() {
    const response = await api.get('/dashboard/stats');
    return response.data;
  },

  async getRecentActivities() {
    const response = await api.get('/dashboard/activities');
    return response.data;
  },

  async getAnalytics(period = '30d') {
    const response = await api.get('/dashboard/analytics', { params: { period } });
    return response.data;
  },
};

// Outreach API
export const outreachService = {
  async sendEmail(candidateId, emailData) {
    const response = await api.post('/outreach/email', {
      candidate_id: candidateId,
      ...emailData,
    });
    return response.data;
  },

  async sendSMS(candidateId, smsData) {
    const response = await api.post('/outreach/sms', {
      candidate_id: candidateId,
      ...smsData,
    });
    return response.data;
  },

  async generateMessage(candidateId, messageType, context) {
    const response = await api.post('/outreach/generate', {
      candidate_id: candidateId,
      message_type: messageType,
      context,
    });
    return response.data;
  },
};

// Calendar API
export const calendarService = {
  async getAvailability(date) {
    const response = await api.get('/calendar/availability', { params: { date } });
    return response.data;
  },

  async createEvent(eventData) {
    const response = await api.post('/calendar/events', eventData);
    return response.data;
  },

  async updateEvent(eventId, eventData) {
    const response = await api.put(`/calendar/events/${eventId}`, eventData);
    return response.data;
  },

  async deleteEvent(eventId) {
    const response = await api.delete(`/calendar/events/${eventId}`);
    return response.data;
  },
};
