import axios from "axios";

const request = axios.create({
    // baseURL: "http://localhost:8000",//test
    baseURL: "http://121.37.88.194:8000",//deploy
});

export default request;
