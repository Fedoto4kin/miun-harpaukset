import axios from '../axios';

export const fetchWordsByLetter = async (letter) => {
  try {
    const response = await axios.get(`v0/lexicon/search/`, {
      params: { letter },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching words by letter:', error);
    throw error;
  }
};

export const fetchWordsBySearch = async (params) => {
  try {
    const url = params.reverse ? `v0/lexicon/reverse/` : `v0/lexicon/search/`;
    const response = await axios.get(url, { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching words by search:', error);
    throw error;
  }
};

export const fetchWordParadigm = async (wordId) => {
  try {
    const response = await axios.get(`v0/lexicon/word-card/${wordId}/paradigm/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching word paradigm:', error);
    throw error;
  }
};