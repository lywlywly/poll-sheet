// appfront/src/api/api.js
import axiosInstance from './index'

const axios = axiosInstance

export const getBooks = () => { return axios.get(`http://localhost:8000/api/books/`) }

export const postBook = (bookName, bookAuthor) => { return axios.post(`http://localhost:8000/api/books/`, { 'name': bookName, 'author': bookAuthor }) }

export const getStudents = () => { return axios.get(`http://127.0.0.1:8000/api/student/`) }

export const postTask = () => {
    return axios.put(`http://localhost:8000/api/tasks/`, {
        "id": 6,
        "title": "otto",
        "description": "world no.1 mid",
    })
}

// export const postStudents = (name, netID, groupID, id) => { return axios.post(`http://127.0.0.1:8000/api/student/`), { 'name': name, 'net_id': netID, 'group_id': groupID, 'id': id } }

export const postStudents = () => {
    return axios.post(`http://127.0.0.1:8000/api/student/`, {
        'id': 15,
        'name': "ll",
        'net_id': "lw",
        'group_id': 1
    })
}

export const putGroupScore = (id, score) => { return axios.put(`http://127.0.0.1:8000/api/group/${id}/`, { 'id': id, 'score': score }) }

export const putFile = (data, id) => { return axios.put(`http://127.0.0.1:8000/api/file/${id}/`, data) }

export const postFile = (data) => { return axios.post(`http://127.0.0.1:8000/api/file/`, data) }

export const getFile = (id) => { return axios.get(`http://127.0.0.1:8000/api/file/${id}/`) }
