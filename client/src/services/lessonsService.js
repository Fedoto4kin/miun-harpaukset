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

export const getModulesByLesson = async (lessonId) => {
  try {
    const response = await axios.get(`v0/modules/by-lesson/${lessonId}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching modules:', error);
    throw error;
  }
};

export const getModuleContent = async (moduleId) => {
  try {
    const response = await axios.get(`v0/modules/${moduleId}/content/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching module content:', error);
    throw error;
  }
};
