import api from './api';

const getJobs = (params) => {
  return api.get('/jobs/', { params });
};

const getJobById = (id) => {
  return api.get(`/jobs/${id}`);
};

const createJob = (jobData) => {
  return api.post('/jobs/', jobData);
};

const updateJob = (id, jobData) => {
  return api.put(`/jobs/${id}`, jobData);
};

const deleteJob = (id) => {
  return api.delete(`/jobs/${id}`);
};

export const jobService = {
  getJobs,
  getJobById,
  createJob,
  updateJob,
  deleteJob,
};
