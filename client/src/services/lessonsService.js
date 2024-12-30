import axios from '../axios';

export const getLessons = async () => {
  try {
    const response = await axios.get('v0/lessons/');
    return response.data;
  } catch (error) {
    console.error('Error fetching lessons:', error);
    throw error;
  }
};