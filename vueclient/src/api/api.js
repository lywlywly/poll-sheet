import axiosInstance from "./index";

const axios = axiosInstance;

export const getStudents = (config) => {
  return axios.get(`http://127.0.0.1:8000/api/student/`, config);
};

export const putFile = (data, id, config) => {
  return axios.put(`http://127.0.0.1:8000/api/file/${id}/`, data, config);
};

export const postFile = (data, config) => {
  return axios.post(`http://127.0.0.1:8000/api/file/`, data, config);
};

export const getFile = (id, config) => {
  return axios.get(`http://127.0.0.1:8000/api/file/${id}/`, config);
};

export const login = (id, pswd) => {
  return axios.post(`http://127.0.0.1:8000/api/v1/dj-rest-auth/login/`, {
    email: id,
    password: pswd,
  });
};

export const getEntries = (config, pollID) => {
  return axios.get(
    `http://127.0.0.1:8000/api/readonly-entry/?poll_id=${pollID}`,
    config
  );
};

export const getAdminEntries = (config) => {
  return axios.get(`http://127.0.0.1:8000/api/entry/`, config);
};

export const getChoices = (config) => {
  return axios.get(`http://127.0.0.1:8000/api/choice/`, config);
};

export const postVote = (data, config) => {
  return axios.post(`http://127.0.0.1:8000/api/vote/`, data, config);
};

// when not logged in as admin, this api only returns your votes
export const getVote = (pollID, config) => {
  return axios.get(`http://127.0.0.1:8000/api/vote/?poll_id=${pollID}`, config);
};

export const deleteVote = (pk, config) => {
  return axios.delete(`http://127.0.0.1:8000/api/vote/${pk}/`, config);
};

export const getCurrentUserInfo = (pollID, config) => {
  return axios.get(`http://127.0.0.1:8000/api/user/?poll_id=${pollID}`, config);
};

export const getGroups = (pollID) => {
  return axios.get(`http://127.0.0.1:8000/api/group/?poll_id=${pollID}`);
};

export const getGroupText = (id) => {
  return axios.get(
    `http://127.0.0.1:8000/api/group_introduction/?group_id=${id}`
  );
};

export const postGroupText = (data, config) => {
  return axios.post(
    `http://127.0.0.1:8000/api/group_introduction/`,
    data,
    config
  );
};
