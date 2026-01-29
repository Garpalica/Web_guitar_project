import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:5000/api",
  withCredentials: true,
});

instance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      originalRequest.url !== "/refresh"
    ) {
      originalRequest._retry = true;

      try {
        await instance.post("/refresh");
        return instance(originalRequest);
      } catch (refreshError) {
        localStorage.clear();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  },
);
export const Axios_Get = async (url) => instance.get(url);
export const Axios_Post = async (url, data) => instance.post(url, data);
export const Axios_Put = async (url, data) => instance.put(url, data);
export const Axios_Delete = async (url, data) =>
  instance.delete(url, { data: data });
