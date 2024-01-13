import axiosInstance from "./index";

const axios = axiosInstance;

const host = "http://127.0.0.1:8000"

export const getStudents = (config) => {
  return axios.get(`${host}/api/student/`, config);
};

export const putFile = (data, id, config) => {
  return axios.put(`${host}/api/file/${id}/`, data, config);
};

export const postFile = (data, config) => {
  return axios.post(`${host}/api/file/`, data, config);
};

export const getFile = (id, config) => {
  return axios.get(`${host}/api/file/${id}/`, config);
};

export const login = (id, pswd) => {
  return axios.post(`${host}/api/v1/dj-rest-auth/login/`, {
    email: id,
    password: pswd,
  });
};

export const getEntries = (config, pollID) => {
  return axios.get(
    `${host}/api/readonly-entry/?poll_id=${pollID}`,
    config
  );
};

export const getAdminEntries = (config) => {
  return axios.get(`${host}/api/entry/`, config);
};

export const getChoices = (config) => {
  return axios.get(`${host}/api/choice/`, config);
};

export const postVote = (data, config) => {
  return axios.post(`${host}/api/vote/`, data, config);
};

// when not logged in as admin, this api only returns your votes
export const getVote = (pollID, config) => {
  return axios.get(`${host}/api/vote/?poll_id=${pollID}`, config);
};

export const deleteVote = (pk, config) => {
  return axios.delete(`${host}/api/vote/${pk}/`, config);
};

export const getCurrentUserInfo = (pollID, config) => {
  return axios.get(`${host}/api/user/?poll_id=${pollID}`, config);
};

export const getGroups = (pollID) => {
  return axios.get(`${host}/api/group/?poll_id=${pollID}`);
};

export const getGroupText = (id) => {
  return axios.get(
    `${host}/api/group_introduction/?group_id=${id}`
  );
};

export const postGroupText = (data, config) => {
  return axios.post(
    `${host}/api/group_introduction/`,
    data,
    config
  );
};

export const getPoll = () => {
  return axios.get(
    `${host}/api/poll/`
  );
};
