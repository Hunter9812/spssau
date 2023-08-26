import axios from "axios";

const request = axios.create({
    // baseURL: "http://localhost:8000",//test
    baseURL: "http://localhost:8090",//deploy
});

export default request;
