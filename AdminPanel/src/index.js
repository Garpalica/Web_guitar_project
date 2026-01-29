import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:5000/api",
  withCredentials: true,
});

export async function Axios_Refresh() {
  try {
    await instance.post("/refresh");
    return true;
  } catch (error) {
    localStorage.clear();
    return false;
  }
}

export async function Axios_Get(url) {
  try {
    const response = await instance.get(url);
    return response;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      const refreshed = await Axios_Refresh();
      if (refreshed) {
        const new_response = await instance.get(url);
        return new_response;
      }
    }
    throw error;
  }
}

export async function Axios_Post(url, data) {
  try {
    const response = await instance.post(url, data);
    return response;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      const refreshed = await Axios_Refresh();
      if (refreshed) {
        const new_response = await instance.post(url, data);
        return new_response;
      }
    }
    throw error;
  }
}

export async function Axios_Put(url, data) {
  try {
    const response = await instance.put(url, data);
    return response;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      const refreshed = await Axios_Refresh();
      if (refreshed) {
        const new_response = await instance.put(url, data);
        return new_response;
      }
    }
    throw error;
  }
}

export async function Axios_Delete(url, data) {
  try {
    const response = await instance.delete(url, { data: data });
    return response;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      const refreshed = await Axios_Refresh();
      if (refreshed) {
        const new_response = await instance.delete(url, { data: data });
        return new_response;
      }
    }
    throw error;
  }
}
